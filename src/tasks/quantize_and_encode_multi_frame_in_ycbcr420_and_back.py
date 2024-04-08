from bitstring import Bits
from collections import Counter
from itertools import chain
from pprint import pprint
from numpy import array, fromiter, load, ravel, uint8, savez
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
    image_data_as_ycbcr_quantized = ()
    for image_data_as_plane in image_data_as_ycbcr:
        image_data_as_plane_quantized = quantize_evenly(
            image_data_as_plane,
            QUANTIZATION_LEVELS,
            *QUANTIZATION_RANGES,
        ).astype(uint8)
        image_data_as_ycbcr_quantized += (image_data_as_plane_quantized,)
    images_data_as_ycbcr_quantized.append(image_data_as_ycbcr_quantized)

# Build a Huffman tree and codebook for the quantized YCbCr images
frequencies_and_quantization_levels = [
    (frequency, level)
    for level, frequency in Counter(
        chain(*map(ravel, chain(*images_data_as_ycbcr_quantized)))
    ).items()
]
coding_tree = HuffmanTree.from_symbolic_frequencies(frequencies_and_quantization_levels)
quantization_levels_and_codes = list(coding_tree.codebook)
quantization_level_to_code_table = dict(quantization_levels_and_codes)

# Encode the quantized YCbCr images using Huffman coding scheme
images_data_as_ycbcr_encoded: List[bytes] = []
for image_data_as_ycbcr_quantized in images_data_as_ycbcr_quantized:
    image_data_as_ycbcr_encoded = ()
    for image_data_as_plane_quantized in image_data_as_ycbcr_quantized:
        image_data_as_plane_encoded = "".join(
            map(
                dict(quantization_levels_and_codes).get,
                image_data_as_plane_quantized.ravel(),
            )
        )
        image_data_as_ycbcr_encoded += (image_data_as_plane_encoded,)
    images_data_as_ycbcr_encoded.append("".join(image_data_as_ycbcr_encoded))
encoded_bits = Bits(bin="".join(images_data_as_ycbcr_encoded))
pprint(encoded_bits[-512:])

# # Save the encoded YCbCr image with the huffman codebook into a bitstream
# bitstream_encoded = (huffman_codebook, images_data_as_ycbcr_encoded)

# # Extract the huffman tree and codebook from the bitstream to decode
# bitstream_to_decode = bitstream_encoded
# huffman_codebook_extracted = bitstream_to_decode[0]
# huffman_tree_extracted = huffman_codebook_extracted

# # Decode the encoded YCbCr image using Huffman coding scheme
# images_data_as_ycbcr_decoded = []
# for image_data_as_ycbcr_to_decode in bitstream_to_decode[0]:
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
images_data_as_ycbcr_decoded = images_data_as_ycbcr_quantized # [TODO]

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
# encoded bitstream

##################
###  Analysis  ###
##################

print(
    """
[Task 3]
    Quantize and encode YCbCr 4:2:0 images and recover them back.
    Below is the mapping table from quantization level to code:
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
