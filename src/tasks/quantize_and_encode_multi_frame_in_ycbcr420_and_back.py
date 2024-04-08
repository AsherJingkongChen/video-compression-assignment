from pprint import pprint
from numpy import uint8
from numpy.typing import NDArray
from typing import List, Tuple, TypeAlias

from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
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
    image_data_as_y, image_data_as_cb, image_data_as_cr = image_data_as_ycbcr

    image_data_as_y_quantized = quantize_evenly(
        image_data_as_y, QUANTIZATION_LEVELS, *QUANTIZATION_RANGES
    ).astype(uint8)
    image_data_as_cb_quantized = quantize_evenly(
        image_data_as_cb, QUANTIZATION_LEVELS, *QUANTIZATION_RANGES
    ).astype(uint8)
    image_data_as_cr_quantized = quantize_evenly(
        image_data_as_cr, QUANTIZATION_LEVELS, *QUANTIZATION_RANGES
    ).astype(uint8)

    images_data_as_ycbcr_quantized.append(
        (
            image_data_as_y_quantized,
            image_data_as_cb_quantized,
            image_data_as_cr_quantized,
        )
    )

# # Build a Huffman tree and codebook for the quantized YCbCr images
# huffman_tree = images_data_as_ycbcr_quantized
# huffman_codebook = huffman_tree

# # Encode the quantized YCbCr image using Huffman coding scheme
# images_data_as_ycbcr_encoded = []
# for image_data_as_ycbcr_quantized in images_data_as_ycbcr_quantized:
#     (
#         image_data_as_y_quantized,
#         image_data_as_cb_quantized,
#         image_data_as_cr_quantized,
#     ) = image_data_as_ycbcr_quantized

#     image_data_as_y_encoded = image_data_as_y_quantized
#     image_data_as_cb_encoded = image_data_as_cb_quantized
#     image_data_as_cr_encoded = image_data_as_cr_quantized
#     image_data_as_ycbcr_encoded = huffman_tree(
#         image_data_as_y_encoded,
#         image_data_as_cb_encoded,
#         image_data_as_cr_encoded,
#     )

#     images_data_as_ycbcr_encoded.append(image_data_as_ycbcr_encoded)

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
    image_data_as_y_decoded, image_data_as_cb_decoded, image_data_as_cr_decoded = (
        image_data_as_ycbcr_decoded
    )

    image_data_as_y_dequantized = quantize_evenly(
        image_data_as_y_decoded, QUANTIZATION_LEVELS, *QUANTIZATION_RANGES[::-1]
    ).astype(uint8)
    image_data_as_cb_dequantized = quantize_evenly(
        image_data_as_cb_decoded, QUANTIZATION_LEVELS, *QUANTIZATION_RANGES[::-1]
    ).astype(uint8)
    image_data_as_cr_dequantized = quantize_evenly(
        image_data_as_cr_decoded, QUANTIZATION_LEVELS, *QUANTIZATION_RANGES[::-1]
    ).astype(uint8)

    images_data_as_ycbcr_dequantized.append(
        (
            image_data_as_y_dequantized,
            image_data_as_cb_dequantized,
            image_data_as_cr_dequantized,
        )
    )

pprint(sorted(set(images_data_as_ycbcr_dequantized[0][0].ravel())))

############################
###  Save the artifacts  ###
############################

# Huffman tree and codebook
# dequantized frames
# decoded frames
# encoded bitstream
