from PIL import Image
from numpy import array, uint8

from ..modules.color import H273, KR_KB_BT601
from ..modules.data import (
    packed_from_planar,
    planar_from_packed,
    save_ycbcr_image,
)
from ..modules.sample import BT2100, SUBSAMPLING_SCHEME_420
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from .utils.report import get_metrics_report

OUTPUTS_DIR_PATH = OUTPUTS_DIR_PATH / "task_1"
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# Load the source image
image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp")

# Ensure that the source image is in the full range RGB color space
image = image.convert("RGB")
image_data_as_drgb = array(image, dtype=uint8)
image_must_be_full_range = (image_data_as_drgb.max() > 219 + 16) or (
    image_data_as_drgb.min() < 16
)
assert (
    image_must_be_full_range
), "The source image is assumed to be in the full range RGB color space"

# Uses ITU-T H.273 and ITU-R BT.601 parameter values
# - The source image is assumed to be gamma-corrected RGB
COLOR = H273()
KR, KB = KR_KB_BT601()

# Uses ITU-R BT.2100 parameter values and sub-sampling scheme 4:2:0
# - The sub-sampling methods are easier to implement
SAMPLE = BT2100()
SUBSAMPLING_SCHEME = SUBSAMPLING_SCHEME_420()

# De-quanitze the image from digital RGB to analog RGB
image_data_as_argb = COLOR.set_full_range(True).dequantize_rgb(image_data_as_drgb)

# Convert the image from analog RGB to YPbPr
image_data_as_ypbpr = COLOR.ypbpr_from_rgb(image_data_as_argb, KR, KB)

# Quantize the image from YPbPr to YCbCr
image_data_as_ycbcr = COLOR.set_full_range(False).quantize_ycbcr(image_data_as_ypbpr)

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

# Up-sample the image in YCbCr color space from 4:2:0 to 4:4:4 scheme
image_data_as_y_upsampled = image_data_as_y_subsampled.copy()
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
image_data_as_ycbcr_upsampled = packed_from_planar(
    (
        image_data_as_y_upsampled,
        image_data_as_cb_upsampled,
        image_data_as_cr_upsampled,
    )
)

# De-quantize the image from YCbCr to YPbPr
image_data_as_ypbpr_transformed = COLOR.set_full_range(False).dequantize_ycbcr(
    image_data_as_ycbcr_upsampled
)

# Convert the image from YPbPr to analog RGB
image_data_as_argb_transformed = COLOR.rgb_from_ypbpr(
    image_data_as_ypbpr_transformed, KR, KB
)

# Quantize the image from analog RGB to digital RGB
image_data_as_drgb_transformed = COLOR.set_full_range(True).quantize_rgb(
    image_data_as_argb_transformed
)

############################
###  Save the artifacts  ###
############################

# Save the copied image in the 24-bit RGB BMP format
# - This is for further comparison with the transformed image
image_copied = Image.fromarray(image_data_as_drgb, mode="RGB")
width, height = image_copied.size
image_copied.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_rgb_copied.{width}x{height}.bmp")

# Save the transformed image in the 24-bit RGB BMP format
image_transformed = Image.fromarray(image_data_as_drgb_transformed, mode="RGB")
width, height = image_transformed.size
image_transformed.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_rgb_transformed.{width}x{height}.bmp"
)

# Save the Y, Cb and Cr images before sub-sampling in the 8-bit grayscale BMP format
image_y = Image.fromarray(image_data_as_y, mode="L")
width, height = image_y.size
image_y.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_y_default.{width}x{height}.bmp")

image_cb = Image.fromarray(image_data_as_cb, mode="L")
width, height = image_cb.size
image_cb.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_cb_default.{width}x{height}.bmp")

image_cr = Image.fromarray(image_data_as_cr, mode="L")
width, height = image_cr.size
image_cr.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_cr_default.{width}x{height}.bmp")

# Save the Y, Cb and Cr images after sub-sampling in the 8-bit grayscale BMP format
image_y_subsampled = Image.fromarray(image_data_as_y_subsampled, mode="L")
width, height = image_y_subsampled.size
image_y_subsampled.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_y_subsampled.{width}x{height}.bmp"
)

image_cb_subsampled = Image.fromarray(image_data_as_cb_subsampled, mode="L")
width, height = image_cb_subsampled.size
image_cb_subsampled.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_cb_subsampled.{width}x{height}.bmp"
)

image_cr_subsampled = Image.fromarray(image_data_as_cr_subsampled, mode="L")
width, height = image_cr_subsampled.size
image_cr_subsampled.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_cr_subsampled.{width}x{height}.bmp"
)

# Save the Y, Cb and Cr images after up-sampling in the 8-bit grayscale BMP format
image_y_upsampled = Image.fromarray(image_data_as_y_upsampled, mode="L")
width, height = image_y_upsampled.size
image_y_upsampled.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_y_upsampled.{width}x{height}.bmp"
)

image_cb_upsampled = Image.fromarray(image_data_as_cb_upsampled, mode="L")
width, height = image_cb_upsampled.size
image_cb_upsampled.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_cb_upsampled.{width}x{height}.bmp"
)

image_cr_upsampled = Image.fromarray(image_data_as_cr_upsampled, mode="L")
width, height = image_cr_upsampled.size
image_cr_upsampled.save(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_cr_upsampled.{width}x{height}.bmp"
)

# Save the sub-sampled YCbCr image in the planar format (YUV420p)
height, width = image_data_as_y_subsampled.shape
with open(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_ycbcr.yuv420p.{width}x{height}.yuv",
    mode="wb",
) as image_ycbcr:
    save_ycbcr_image(
        image_ycbcr,
        (
            image_data_as_y_subsampled,
            image_data_as_cb_subsampled,
            image_data_as_cr_subsampled,
        ),
    )

################
###  Report  ###
################

print(
    f"""\
# Assignment 1 Code Outputs

## Reproduction

1. Install the requirements
```shell
python3 -m pip install -Ur requirements.txt
```

2. Run all the tasks
```shell
python3 run_tasks.py
```

## Task 1

Convert an image from RGB to YCbCr `4:2:0` and recover it.

*Assume that the copied image is equivalent to the original image.*

### Visual Comparison

Display images.

I added transformed images from YCbCr to RGB using `utils/YUVDisplay.exe`.

There are the images in the RGB color space below.

| Copied Image | Transformed Image (Mine) | Transformed Image (YUVDisplay.exe) |
| ------------ | ------------------------ | ---------------------------------- |
| ![](./task_1/foreman_qcif_0_rgb_copied.176x144.bmp) | ![](./task_1/foreman_qcif_0_rgb_transformed.176x144.bmp) | ![](./task_1/foreman_qcif_0_ycbcr.yuv420p.176x144.yuv.bmp) |

There are the images in the YCbCr color space re-mapped to the grayscale colorspace below.

|             | Before sub-sampling | After sub-sampling | After up-sampling |
| ----------- | ------------------- | ------------------ | ----------------- |
| On Y plane  | ![](./task_1/foreman_qcif_0_y_default.176x144.bmp)  | ![](./task_1/foreman_qcif_0_y_subsampled.176x144.bmp) | ![](./task_1/foreman_qcif_0_y_upsampled.176x144.bmp)  |
| On Cb plane | ![](./task_1/foreman_qcif_0_cb_default.176x144.bmp) | ![](./task_1/foreman_qcif_0_cb_subsampled.88x72.bmp)  | ![](./task_1/foreman_qcif_0_cb_upsampled.176x144.bmp) |
| On Cr plane | ![](./task_1/foreman_qcif_0_cr_default.176x144.bmp) | ![](./task_1/foreman_qcif_0_cr_subsampled.88x72.bmp)  | ![](./task_1/foreman_qcif_0_cr_upsampled.176x144.bmp) |

### Statistical Comparison

Compare between the copied and transformed images in the RGB color space.

There are the metric results computed
between the copied and transformed images below.

{get_metrics_report(image_copied, image_transformed)}

### Details

The process workflow is as follows.

```mermaid
graph LR
    drgb[/Digital RGB image 0~255/]
    argb([Analog RGB image 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr image 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr image 16~235; 16~240/]
    sub[Sub-sampling to 4:2:0]
    ups[Up-sampling from 4:2:0 to 4:4:4]

    drgb -->|1| argb
    argb -->|2| tran
    tran -->|3| ayuv
    ayuv -->|4| dyuv
    dyuv -->|5| sub
    sub -->|6| ups
    ups -->|7| dyuv
    dyuv -->|8| ayuv
    ayuv -->|9| tran
    tran -->|10| argb
    argb -->|11| drgb
```
"""
)
