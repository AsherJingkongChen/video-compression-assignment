from bitstring import Bits, ConstBitStream
from collections import Counter
from itertools import chain
from numpy import (
    asarray,
    array_equal,
    empty,
    load,
    ravel,
    uint8,
    uint64,
    savez,
)
from numpy.typing import NDArray
from PIL import Image
from typing import List, Tuple, TypeAlias

from .utils.env import OUTPUTS_DIR_PATH
from .utils.report import get_metrics_report
from ..modules.coding import HuffmanTree
from ..modules.data import packed_from_planar
from ..modules.quant import quantize_evenly

OUTPUTS_DIR_PATH = OUTPUTS_DIR_PATH / "task_3"
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# Uses the values in the previous task
from .convert_multi_frame_from_rgb_to_ycbcr420 import (
    images_data_as_ycbcr,
    COLOR,
    KR,
    KB,
    SAMPLE,
    SUBSAMPLING_SCHEME,
)

ImagesData: TypeAlias = List[Tuple[NDArray[uint8], NDArray[uint8], NDArray[uint8]]]

# Uses 16 levels (0 to 15) to quantize 225 possible intensities (16 to 240)
# - Y, Cb and Cr components are 8-bit unsigned integers
QUANTIZATION_LEVELS = 16
QUANTIZATION_RANGES = [(16, 240), (0, QUANTIZATION_LEVELS - 1)]

# Quantize the YCbCr images to 16 levels evenly
images_data_as_ycbcr_quantized: ImagesData = []
for image_data_as_ycbcr in images_data_as_ycbcr:
    image_data_as_ycbcr_quantized: Tuple[NDArray[uint8], ...] = ()
    for image_data_as_plane in image_data_as_ycbcr:
        image_data_as_plane_quantized = quantize_evenly(
            image_data_as_plane,
            QUANTIZATION_LEVELS,
            *QUANTIZATION_RANGES,
        ).astype(uint8)

        image_data_as_ycbcr_quantized += (image_data_as_plane_quantized,)

    images_data_as_ycbcr_quantized.append(image_data_as_ycbcr_quantized)

# Build a Huffman tree and code table for the quantized YCbCr images
frequencies_and_quantization_levels = asarray(
    [
        (frequency, level)
        for level, frequency in Counter(
            chain(*map(ravel, chain(*images_data_as_ycbcr_quantized)))
        ).items()
    ]
)
coding_tree: HuffmanTree[uint8] = HuffmanTree.from_symbolic_frequencies(
    frequencies_and_quantization_levels
)

# Encode the quantized YCbCr images using Huffman coding scheme
# - Gather metadata of the encoded images
images_data_as_ycbcr_encoded: List[Tuple[str, str, str]] = []
images_bitlen_as_ycbcr_encoded: List[Tuple[int, int, int]] = []
images_shape_as_ycbcr_encoded: List[
    Tuple[Tuple[int, ...], Tuple[int, ...], Tuple[int, ...]]
] = []
for image_data_as_ycbcr_quantized in images_data_as_ycbcr_quantized:
    image_data_as_ycbcr_encoded: Tuple[str, ...] = ()
    image_bitlen_as_ycbcr_encoded: Tuple[int, ...] = ()
    image_shape_as_ycbcr_encoded: Tuple[Tuple[int, ...], ...] = ()
    for image_data_as_plane_quantized in image_data_as_ycbcr_quantized:
        image_data_as_plane_encoded = "".join(
            map(coding_tree.encode, image_data_as_plane_quantized.ravel())
        )
        image_bitlen_as_plane_encoded = len(image_data_as_plane_encoded)
        image_shape_as_plane_encoded = image_data_as_plane_quantized.shape

        image_data_as_ycbcr_encoded += (image_data_as_plane_encoded,)
        image_bitlen_as_ycbcr_encoded += (image_bitlen_as_plane_encoded,)
        image_shape_as_ycbcr_encoded += (image_shape_as_plane_encoded,)

    images_data_as_ycbcr_encoded.append(image_data_as_ycbcr_encoded)
    images_bitlen_as_ycbcr_encoded.append(image_bitlen_as_ycbcr_encoded)
    images_shape_as_ycbcr_encoded.append(image_shape_as_ycbcr_encoded)

# Save the encoded YCbCr images with their metadata and the huffman code table into a bundle
images_data_as_ycbcr_encoded_chained = Bits(
    bin="".join(chain(*images_data_as_ycbcr_encoded))
)

bundle_path = OUTPUTS_DIR_PATH / "foreman_qcif_0-2_ycbcr.yuv420p.yuv.huffman.npz"
savez(
    bundle_path,
    images_data_as_ycbcr_encoded_chained=asarray(
        images_data_as_ycbcr_encoded_chained.tobytes()
    ),
    images_bitlen_as_ycbcr_encoded=asarray(
        images_bitlen_as_ycbcr_encoded,
        dtype=uint64,
    ),
    images_shape_as_ycbcr_encoded=asarray(
        images_shape_as_ycbcr_encoded,
        dtype=uint64,
    ),
    coding_tree_source=frequencies_and_quantization_levels,
)

# Load the bundle and recover the encoded images, metadata and huffman code table
bundle = load(bundle_path, mmap_mode="r")
coding_tree_re: HuffmanTree[uint8] = HuffmanTree.from_symbolic_frequencies(
    bundle["coding_tree_source"]
)
images_data_as_ycbcr_encoded_chained_re = ConstBitStream(
    bundle["images_data_as_ycbcr_encoded_chained"].tobytes()
)

# Decode the encoded YCbCr images using the Huffman coding scheme
images_data_as_ycbcr_decoded: ImagesData = []
for image_bitlen_as_ycbcr_encoded_re, image_shape_as_ycbcr_encoded_re in zip(
    bundle["images_bitlen_as_ycbcr_encoded"],
    bundle["images_shape_as_ycbcr_encoded"],
):
    image_data_as_ycbcr_decoded: Tuple[NDArray[uint8], ...] = ()
    for image_bitlen_as_plane_encoded_re, image_shape_as_plane_encoded_re in zip(
        image_bitlen_as_ycbcr_encoded_re,
        image_shape_as_ycbcr_encoded_re,
    ):
        image_data_as_plane_encoded_re = (
            images_data_as_ycbcr_encoded_chained_re.read(
                image_bitlen_as_plane_encoded_re.item()
            )
            .tobitarray()
            .to01()
        )
        image_data_as_plane_decoded = empty(
            shape=image_shape_as_plane_encoded_re, dtype=uint8
        )
        index = 0
        image_data_as_plane_decoded_flatten = image_data_as_plane_decoded.ravel()
        while image_data_as_plane_encoded_re:
            quantization_level_re, image_data_as_plane_encoded_re = (
                coding_tree_re.decode(image_data_as_plane_encoded_re)
            )
            image_data_as_plane_decoded_flatten[index] = quantization_level_re
            index += 1

        image_data_as_ycbcr_decoded += (image_data_as_plane_decoded,)

    images_data_as_ycbcr_decoded.append(image_data_as_ycbcr_decoded)

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

# 1. Up-sample the de-quantized YCbCr images from 4:2:0 to 4:4:4 scheme
# 2. De-quantize the image from YCbCr to YPbPr
# 3. Convert the image from YPbPr to analog RGB
# 4. Quantize the image from analog RGB to digital RGB
# - For comparison purposes
images_data_as_drgb_upsampled: List[NDArray[uint8]] = []
for image_data_as_ycbcr_dequantized in images_data_as_ycbcr_dequantized:
    # 1. ...
    (
        image_data_as_y_dequantized,
        image_data_as_cb_dequantized,
        image_data_as_cr_dequantized,
    ) = image_data_as_ycbcr_dequantized
    image_data_as_y_upsampled = image_data_as_y_dequantized.copy()
    image_data_as_cb_upsampled = SAMPLE.upsample(
        SUBSAMPLING_SCHEME,
        image_data_as_y_dequantized,
        image_data_as_cb_dequantized,
    )
    image_data_as_cr_upsampled = SAMPLE.upsample(
        SUBSAMPLING_SCHEME,
        image_data_as_y_dequantized,
        image_data_as_cr_dequantized,
    )
    image_data_as_ycbcr_upsampled = packed_from_planar(
        (
            image_data_as_y_upsampled,
            image_data_as_cb_upsampled,
            image_data_as_cr_upsampled,
        )
    )

    # 2. ...
    image_data_as_ypbpr_upsampled = COLOR.set_full_range(False).dequantize_ycbcr(
        image_data_as_ycbcr_upsampled
    )

    # 3. ...
    image_data_as_argb_upsampled = COLOR.rgb_from_ypbpr(
        image_data_as_ypbpr_upsampled, KR, KB
    )

    # 4. ...
    image_data_as_drgb_upsampled = COLOR.set_full_range(True).quantize_rgb(
        image_data_as_argb_upsampled
    )

    images_data_as_drgb_upsampled.append(image_data_as_drgb_upsampled)

############################
###  Save the artifacts  ###
############################

# Save the transformed images (de-quantized and up-sampled) in the 24-bit RGB BMP format
for i, image_data_as_drgb_upsampled in enumerate(images_data_as_drgb_upsampled):
    image_as_drgb_upsampled = Image.fromarray(image_data_as_drgb_upsampled, mode="RGB")
    width, height = image_as_drgb_upsampled.size
    image_as_drgb_upsampled.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_rgb_transformed.{width}x{height}.bmp"
    )

# Save the Y, Cb and Cr images before quantization in the 8-bit grayscale BMP format
images_as_ycbcr: List[Tuple[Image.Image, Image.Image, Image.Image]] = []
for i, image_data_as_ycbcr in enumerate(images_data_as_ycbcr):
    (
        image_data_as_y,
        image_data_as_cb,
        image_data_as_cr,
    ) = image_data_as_ycbcr

    image_as_y = Image.fromarray(image_data_as_y, mode="L")
    width, height = image_as_y.size
    image_as_y.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_y_before_quantized.{width}x{height}.bmp"
    )

    image_as_cb = Image.fromarray(image_data_as_cb, mode="L")
    width, height = image_as_cb.size
    image_as_cb.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_cb_before_quantized.{width}x{height}.bmp"
    )
    
    image_as_cr = Image.fromarray(image_data_as_cr, mode="L")
    width, height = image_as_cr.size
    image_as_cr.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_cr_before_quantized.{width}x{height}.bmp"
    )
    
    images_as_ycbcr.append((image_as_y, image_as_cb, image_as_cr))

# Save the Y, Cb and Cr images after quantization and de-quantization in the 8-bit grayscale BMP format
images_as_ycbcr_dequantized: List[Tuple[Image.Image, Image.Image, Image.Image]] = []
for i, image_data_as_ycbcr_dequantized in enumerate(images_data_as_ycbcr_dequantized):
    (
        image_data_as_y_dequantized,
        image_data_as_cb_dequantized,
        image_data_as_cr_dequantized,
    ) = image_data_as_ycbcr_dequantized

    image_as_y_dequantized = Image.fromarray(image_data_as_y_dequantized, mode="L")
    width, height = image_as_y_dequantized.size
    image_as_y_dequantized.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_y_dequantized.{width}x{height}.bmp"
    )

    image_as_cb_dequantized = Image.fromarray(image_data_as_cb_dequantized, mode="L")
    width, height = image_as_cb_dequantized.size
    image_as_cb_dequantized.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_cb_dequantized.{width}x{height}.bmp"
    )

    image_as_cr_dequantized = Image.fromarray(image_data_as_cr_dequantized, mode="L")
    width, height = image_as_cr_dequantized.size
    image_as_cr_dequantized.save(
        OUTPUTS_DIR_PATH / f"foreman_qcif_{i}_cr_dequantized.{width}x{height}.bmp"
    )

    images_as_ycbcr_dequantized.append((
        image_as_y_dequantized,
        image_as_cb_dequantized,
        image_as_cr_dequantized,
    ))

################
###  Report  ###
################

# Ensure that the recovered huffman tree is equal to the original one
assert coding_tree.equal(coding_tree_re)

# Ensure that the decoded YCbCr images are equal to the quantized YCbCr images
assert bool(images_data_as_ycbcr_quantized) and len(
    images_data_as_ycbcr_quantized
) == len(images_data_as_ycbcr_decoded)
assert bool(images_data_as_ycbcr_quantized[0]) and len(
    images_data_as_ycbcr_quantized[0]
) == len(images_data_as_ycbcr_decoded[0])

for image_data_as_ycbcr_quantized, image_data_as_ycbcr_decoded in zip(
    images_data_as_ycbcr_quantized, images_data_as_ycbcr_decoded
):
    for image_data_as_plane_quantized, image_data_as_plane_decoded in zip(
        image_data_as_ycbcr_quantized, image_data_as_ycbcr_decoded
    ):
        assert array_equal(
            image_data_as_plane_quantized, image_data_as_plane_decoded
        ), (
            image_data_as_plane_quantized,
            image_data_as_plane_decoded,
        )

print(
    f"""\
## Task 3

Quantize in 16 levels and encode YCbCr `4:2:0` images and recover them.

Uses Huffman coding scheme.

### Visual Comparison

Display structures and images.

There are 16 symbols in Huffman code table as the number of quantization levels.

There are the code table and tree diagram of the Huffman tree used below.

{coding_tree}

I added assertion checks to ensure that
the decoded images are equal to the quantized images.
(See the module `{__name__}`)

I added the up-sampled images for comparison purposes
since they have the same size as the original ones.
{"".join(
        f'''
The images with sequence number `{id}` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image |
| -------------- | ----------------- |
| ![](../assets/foreman_qcif_{id}_rgb.bmp) | ![](./task_3/foreman_qcif_{id}_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_{id}_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_{id}_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_{id}_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_{id}_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_{id}_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_{id}_cr_dequantized.88x72.bmp)  |
'''
    for id in range(3)
)}
### Statistical Comparison
{"".join(
        f'''
The image pair with sequence number `{id}`:

On the Y plane:

{get_metrics_report(images_as_ycbcr[id][0], images_as_ycbcr_dequantized[id][0])}

On the Cb plane:

{get_metrics_report(images_as_ycbcr[id][1], images_as_ycbcr_dequantized[id][1])}

On the Cr plane:

{get_metrics_report(images_as_ycbcr[id][2], images_as_ycbcr_dequantized[id][2])}
'''
    for id in range(3)
)}
### Details

The process workflow is as follows.

```mermaid
graph LR
    dyuv[/Digital YCbCr images 16~235; 16~240/]
    sub[Sub-sampling to 4:2:0]
    qua[Quantization in 16 levels from 16~240]
    enc[Encoding using Huffman coding]
    bun[Bundle the encoded images with metadata]
    ubu[Un-bundle the encoded images with metadata]
    dec[Decoding using Huffman coding]
    dqu[De-quantization in 16 levels to 16~240]
    ups[Up-sampling from 4:2:0 to 4:4:4]

    dyuv -->|1| sub
    sub -->|2| qua
    qua -->|3| enc
    enc -->|4| bun
    bun -->|5| ubu
    ubu -->|6| dec
    dec -->|7| dqu
    dqu -->|8| ups
    ups -->|9| dyuv
```
"""
)
