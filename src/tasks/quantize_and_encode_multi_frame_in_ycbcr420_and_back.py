from bitstring import Bits, ConstBitStream
from collections import Counter
from itertools import chain
from pprint import pprint
from numpy import asarray, load, ravel, uint8, uint32, uint64, savez
from numpy.typing import NDArray
from typing import List, Tuple, TypeAlias

from .utils.env import OUTPUTS_DIR_PATH
from ..modules.coding import HuffmanTree
from ..modules.quant import quantize_evenly
from ..modules.sample import SUBSAMPLING_SCHEME_420

OUTPUTS_DIR_PATH = OUTPUTS_DIR_PATH / "task_3"
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# Uses the values in the previous task
from .convert_multi_frame_from_rgb_to_ycbcr420 import images_data_as_ycbcr

ImagesData: TypeAlias = List[Tuple[NDArray[uint8], NDArray[uint8], NDArray[uint8]]]

# Uses sub-sampling scheme 4:2:0
SUBSAMPLING_SCHEME = SUBSAMPLING_SCHEME_420()

# Uses 16 levels (0 to 15) to quantize 225 possible intensities (16 to 240)
# - Y, Cb and Cr components are 8-bit unsigned integers
QUANTIZATION_LEVELS = 16
QUANTIZATION_RANGES = [(16, 240), (0, QUANTIZATION_LEVELS - 1)]

# Quantize the YCbCr images to 16 levels evenly
images_data_as_ycbcr_quantized: ImagesData = []
for image_data_as_ycbcr in images_data_as_ycbcr:
    image_data_as_ycbcr_quantized: Tuple[NDArray, ...] = ()
    for image_data_as_plane in image_data_as_ycbcr:
        image_data_as_plane_quantized = quantize_evenly(
            image_data_as_plane,
            QUANTIZATION_LEVELS,
            *QUANTIZATION_RANGES,
        ).astype(uint8)
        image_data_as_ycbcr_quantized += (image_data_as_plane_quantized,)
    images_data_as_ycbcr_quantized.append(image_data_as_ycbcr_quantized)

# Build a Huffman tree and codebook for the quantized YCbCr images
frequencies_and_quantization_levels = asarray(
    [
        (frequency, level)
        for level, frequency in Counter(
            chain(*map(ravel, chain(*images_data_as_ycbcr_quantized)))
        ).items()
    ]
)
coding_tree = HuffmanTree.from_symbolic_frequencies(frequencies_and_quantization_levels)
quantization_level_to_code_table = dict(coding_tree.codebook)

# Encode the quantized YCbCr images using Huffman coding scheme
# - Gather metadata of the encoded images
images_data_as_ycbcr_encoded: List[Tuple[Bits, Bits, Bits]] = []
images_bitlen_as_ycbcr_encoded: List[Tuple[int, int, int]] = []
images_shape_as_ycbcr_encoded: List[
    Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]
] = []
for image_data_as_ycbcr_quantized in images_data_as_ycbcr_quantized:
    image_data_as_ycbcr_encoded: Tuple[Bits, ...] = ()
    image_bitlen_as_ycbcr_encoded: Tuple[int, ...] = ()
    image_shape_as_ycbcr_encoded: Tuple[Tuple[int, ...], ...] = ()
    for image_data_as_plane_quantized in image_data_as_ycbcr_quantized:
        image_data_as_plane_encoded = Bits(
            bin="".join(
                map(
                    quantization_level_to_code_table.get,
                    image_data_as_plane_quantized.ravel(),
                )
            )
        )
        image_bitlen_as_plane_encoded = len(image_data_as_plane_encoded)
        image_shape_as_plane_encoded = image_data_as_plane_quantized.shape
        image_data_as_ycbcr_encoded += (image_data_as_plane_encoded,)
        image_bitlen_as_ycbcr_encoded += (image_bitlen_as_plane_encoded,)
        image_shape_as_ycbcr_encoded += (image_shape_as_plane_encoded,)
    images_data_as_ycbcr_encoded.append(image_data_as_ycbcr_encoded)
    images_bitlen_as_ycbcr_encoded.append(image_bitlen_as_ycbcr_encoded)
    images_shape_as_ycbcr_encoded.append(image_shape_as_ycbcr_encoded)

# Save the encoded YCbCr images with their metadata
# and the huffman codebook into a bundle.
images_data_as_ycbcr_encoded_chained = Bits().join(chain(*images_data_as_ycbcr_encoded))

bundle_path = OUTPUTS_DIR_PATH / "foreman_qcif_0-2_huffman-encoded.ycbcr.yuv420p.npz"
savez(
    bundle_path,
    images_data_as_ycbcr_encoded_chained=asarray(
        images_data_as_ycbcr_encoded_chained.tobytes()
    ),
    images_bitlen_as_ycbcr_encoded=asarray(
        images_bitlen_as_ycbcr_encoded, dtype=uint64
    ),
    images_shape_as_ycbcr_encoded=asarray(images_shape_as_ycbcr_encoded, dtype=uint32),
    coding_tree_source=frequencies_and_quantization_levels,
)

print(len(images_data_as_ycbcr_encoded_chained))

# Load the bundle and extract the encoded bits, metadata and huffman codebook
bundle = load(bundle_path, mmap_mode="r")
coding_tree_re = HuffmanTree.from_symbolic_frequencies(bundle["coding_tree_source"])
code_to_quantization_level_table_re = {
    Bits(bin=code): symbol for symbol, code in coding_tree_re.codebook
}

images_data_as_ycbcr_encoded_chained_re = ConstBitStream(
    bundle["images_data_as_ycbcr_encoded_chained"].tobytes()
)
for image_bitlen_as_ycbcr_encoded_re, image_shape_as_ycbcr_encoded_re in zip(
    bundle["images_bitlen_as_ycbcr_encoded"].ravel(),
    bundle["images_shape_as_ycbcr_encoded"].reshape(-1, 2),
):
    images_data_as_ycbcr_encoded_re = images_data_as_ycbcr_encoded_chained_re.read(
        image_bitlen_as_ycbcr_encoded_re.item()
    )
    encoded_bits = images_data_as_ycbcr_encoded_re
    print(len(encoded_bits))
    # while images_data_as_ycbcr_encoded_re:
    #     for code, quantization_level in code_to_quantization_level_table_re.items():
    #         if images_data_as_ycbcr_encoded_re.startswith(code):
    #             res += quantization_level
    #             images_data_as_ycbcr_encoded_re = images_data_as_ycbcr_encoded_re[len(code):]

# images_data_as_encoded_bits_re = Bits(bundle["images_data_as_encoded_bits"].tobytes())[
#     : bundle["length_of_images_data_as_encoded_bits"].item()
# ]
# coding_tree_re = HuffmanTree.from_symbolic_frequencies(bundle["coding_tree_source"])
# quantization_level_to_code_table_re = dict(coding_tree_re.codebook)

# assert images_data_as_encoded_bits == images_data_as_encoded_bits_re
# assert quantization_level_to_code_table == quantization_level_to_code_table_re

# # Decode the encoded YCbCr image using Huffman coding scheme
# images_data_as_ycbcr_decoded = []
# for image_data_as_ycbcr_to_decode in Constbitstream_to_decode[0]:
#     image_data_as_ycbcr_decoded = (
#         huffman_tree_extracted,
#         image_data_as_ycbcr_to_decode,
#     )
#     (
#         image_data_as_y_decoded,
#         image_data_as_cb_decoded,
#         image_data_as_cr_decoded,
#     ) = image_data_as_ycbcr_decoded

#     images_data_as_ycbcr_decoded.append(
#         (
#             image_data_as_y_decoded,
#             image_data_as_cb_decoded,
#             image_data_as_cr_decoded,
#         )
#     )
images_data_as_ycbcr_decoded = images_data_as_ycbcr_quantized  # [TODO]

# De-quantize the decoded YCbCr images in 16 levels evenly
images_data_as_ycbcr_dequantized: ImagesData = []
for image_data_as_ycbcr_decoded in images_data_as_ycbcr_decoded:
    image_data_as_ycbcr_dequantized = ()
    for image_data_as_plane_decoded in image_data_as_ycbcr_decoded:
        image_data_as_plane_dequantized = quantize_evenly(
            image_data_as_plane_decoded,
            QUANTIZATION_LEVELS,
            *QUANTIZATION_RANGES[::-1],
        ).astype(uint8)
        image_data_as_ycbcr_dequantized += (image_data_as_plane_dequantized,)
    images_data_as_ycbcr_dequantized.append(image_data_as_ycbcr_dequantized)

############################
###  Save the artifacts  ###
############################

# Huffman tree and codebook
# dequantized frames
# decoded frames
# encoded Constbitstream

##################
###  Analysis  ###
##################

print(
    """
[Task 3]
    Quantize and encode YCbCr 4:2:0 images and recover them back.
    Below is the Huffman codebook from quantization level to code:
"""
)
pprint(quantization_level_to_code_table)
print(
    """
    Below is the Huffman coding tree in Mermaid diagram syntax:

```mermaid

Graph TD\
"""
)
# pprint(coding_tree)
print("```")
