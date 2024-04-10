from PIL import Image
from numpy import array, uint8
from numpy.typing import NDArray
from typing import List, Tuple

from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from .utils.report import get_metrics_report
from ..modules.color import H273, KR_KB_BT601
from ..modules.data import planar_from_packed, save_ycbcr_image
from ..modules.sample import BT2100, SUBSAMPLING_SCHEME_420

__all__ = ["images_data_as_ycbcr"]
OUTPUTS_DIR_PATH = OUTPUTS_DIR_PATH / "task_2"
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# The sub-sampled YCbCr images will be saved in the memory
# - The next task will use these images
images_data_as_ycbcr: List[
    Tuple[
        NDArray[uint8],
        NDArray[uint8],
        NDArray[uint8],
    ]
] = []

# The images will be saved in the memory for statistical comparison
images_as_ycbcr: List[Tuple[Image.Image, Image.Image, Image.Image]] = []
images_as_ycbcr_upsampled: List[Tuple[Image.Image, Image.Image, Image.Image]] = []

# Uses ITU-T H.273 and ITU-R BT.601 parameter values
# - The source image is assumed to be gamma-corrected RGB
COLOR = H273()
KR, KB = KR_KB_BT601()

# Uses ITU-R BT.2100 parameter values and sub-sampling scheme 4:2:0
# - The sub-sampling methods are easier to implement
SAMPLE = BT2100()
SUBSAMPLING_SCHEME = SUBSAMPLING_SCHEME_420()

for image_id in range(3):
    # Load the source image
    image = Image.open(ASSETS_DIR_PATH / f"foreman_qcif_{image_id}_rgb.bmp")

    # Ensure that the source image is in the full range RGB color space
    image = image.convert("RGB")
    image_data_as_drgb = array(image, dtype=uint8)
    image_must_be_full_range = (image_data_as_drgb.max() > 219 + 16) or (
        image_data_as_drgb.min() < 16
    )
    assert (
        image_must_be_full_range
    ), "The source image is assumed to be in the full range RGB color space"

    # De-quanitze the image from digital RGB to analog RGB
    image_data_as_argb = COLOR.set_full_range(True).dequantize_rgb(image_data_as_drgb)

    # Convert the image from analog RGB to YPbPr
    image_data_as_ypbpr = COLOR.ypbpr_from_rgb(image_data_as_argb, KR, KB)

    # Quantize the image from YPbPr to YCbCr
    image_data_as_ycbcr = COLOR.set_full_range(False).quantize_ycbcr(
        image_data_as_ypbpr
    )

    # Sub-sample the image in YCbCr color space using 4:2:0 scheme
    image_data_as_y, image_data_as_cb, image_data_as_cr = planar_from_packed(
        image_data_as_ycbcr
    )
    image_data_as_y_subsampled = image_data_as_y.copy()
    image_data_as_cb_subsampled = SAMPLE.subsample(
        SUBSAMPLING_SCHEME,
        image_data_as_y,
        image_data_as_cb,
    )
    image_data_as_cr_subsampled = SAMPLE.subsample(
        SUBSAMPLING_SCHEME,
        image_data_as_y,
        image_data_as_cr,
    )

    # Save the multiple sub-sampled YCbCr images
    # in the memory for the next task
    images_data_as_ycbcr.append(
        (
            image_data_as_y_subsampled,
            image_data_as_cb_subsampled,
            image_data_as_cr_subsampled,
        )
    )

    # Up-sample the sub-sampled image in YCbCr color space using 4:2:0 scheme
    # - For comparison purposes
    image_data_as_y_upsampled = image_data_as_y.copy()
    image_data_as_cb_upsampled = SAMPLE.upsample(
        SUBSAMPLING_SCHEME,
        image_data_as_y_subsampled,
        image_data_as_cb_subsampled,
    )
    image_data_as_cr_upsampled = SAMPLE.upsample(
        SUBSAMPLING_SCHEME,
        image_data_as_y_subsampled,
        image_data_as_cr_subsampled,
    )

    ############################
    ###  Save the artifacts  ###
    ############################

    # Save the Y, Cb and Cr images without sub-sampling in the 8-bit grayscale BMP format
    image_y = Image.fromarray(image_data_as_y, mode="L")
    width, height = image_y.size
    image_y.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_y_without_subsampling.{width}x{height}.bmp"
    )

    image_cb = Image.fromarray(image_data_as_cb, mode="L")
    width, height = image_cb.size
    image_cb.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_cb_without_subsampling.{width}x{height}.bmp"
    )

    image_cr = Image.fromarray(image_data_as_cr, mode="L")
    width, height = image_cr.size
    image_cr.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_cr_without_subsampling.{width}x{height}.bmp"
    )

    # Save the Y, Cb and Cr images with sub-sampling in the 8-bit grayscale BMP format
    image_y_subsampled = Image.fromarray(image_data_as_y_subsampled, mode="L")
    width, height = image_y_subsampled.size
    image_y_subsampled.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_y_with_subsampling.{width}x{height}.bmp"
    )

    image_cb_subsampled = Image.fromarray(image_data_as_cb_subsampled, mode="L")
    width, height = image_cb_subsampled.size
    image_cb_subsampled.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_cb_with_subsampling.{width}x{height}.bmp"
    )

    image_cr_subsampled = Image.fromarray(image_data_as_cr_subsampled, mode="L")
    width, height = image_cr_subsampled.size
    image_cr_subsampled.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_cr_with_subsampling.{width}x{height}.bmp"
    )

    # Save the Y, Cb and Cr images with up-sampling in the 8-bit grayscale BMP format
    image_y_upsampled = Image.fromarray(image_data_as_y_upsampled, mode="L")
    width, height = image_y_upsampled.size
    image_y_upsampled.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_y_with_upsampling.{width}x{height}.bmp"
    )

    image_cb_upsampled = Image.fromarray(image_data_as_cb_upsampled, mode="L")
    width, height = image_cb_upsampled.size
    image_cb_upsampled.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_cb_with_upsampling.{width}x{height}.bmp"
    )

    image_cr_upsampled = Image.fromarray(image_data_as_cr_upsampled, mode="L")
    width, height = image_cr_upsampled.size
    image_cr_upsampled.save(
        OUTPUTS_DIR_PATH
        / f"foreman_qcif_{image_id}_cr_with_upsampling.{width}x{height}.bmp"
    )

    images_as_ycbcr.append((image_y, image_cb, image_cr))
    images_as_ycbcr_upsampled.append(
        (image_y_upsampled, image_cb_upsampled, image_cr_upsampled)
    )

# Save the sub-sampled YCbCr image in the planar format (YUV420p)
height, width = images_data_as_ycbcr[0][0].shape
with open(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0-2_ycbcr.yuv420p.{width}x{height}.yuv",
    mode="wb",
) as images_ycbcr:
    for image_data_ycbcr in images_data_as_ycbcr:
        save_ycbcr_image(images_ycbcr, image_data_ycbcr)

################
###  Report  ###
################

print(
    """\
## Task 2

Convert the multiple images from RGB to YCbCr `4:2:0` color space
and pack them into a file in planar format.

### Visual Comparison

Display images.

I added the up-sampled images and re-exported them using `utils/YUVDisplay.exe`
for comparison purposes since they have the same size as the original ones.
"""
)
print(
    "".join(
        f"""\
The images with sequence number `{id}` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_{id}_rgb.bmp) | ![](./task_2/foreman_qcif_{id}_ycbcr.yuv420p.176x144.yuv.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_{id}_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_{id}_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_{id}_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_{id}_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_{id}_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_{id}_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_{id}_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_{id}_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_{id}_cr_with_upsampling.176x144.bmp) |
"""
        for id in range(3)
    )
)
print(
    """\
### Statistical Comparison

Compare between the images without sub-sampling and with sub-sampling
in the YCbCr color space.

There are the metric results computed
between the copied and transformed images below.
"""
)
print(
    "".join(
        f"""\
The image pair with sequence number `{id}`:

On the Y plane:

{get_metrics_report(images_as_ycbcr[id][0], images_as_ycbcr_upsampled[id][0])}

On the Cb plane:

{get_metrics_report(images_as_ycbcr[id][1], images_as_ycbcr_upsampled[id][1])}

On the Cr plane:

{get_metrics_report(images_as_ycbcr[id][2], images_as_ycbcr_upsampled[id][2])}
"""
        for id in range(3)
    )
)
print(
    """\
### Details

The process workflow is as follows.

```mermaid
graph LR
    drgb[/Digital RGB images 0~255/]
    argb([Analog RGB images 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr images 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr images 16~235; 16~240/]
    sub[Sub-sampling to 4:2:0]
    ups[Up-sampling from 4:2:0 to 4:4:4]
    pack[Pack YCbCr images in YUV420p format]

    drgb -->|1| argb
    argb -->|2| tran
    tran -->|3| ayuv
    ayuv -->|4| dyuv
    dyuv -->|5| sub
    sub -->|6| pack
    sub -->|7| ups
    ups -->|8| dyuv
```
"""
)
