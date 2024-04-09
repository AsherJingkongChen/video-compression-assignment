from PIL import Image
from numpy import array, array_equal, uint8
from numpy.typing import NDArray
from typing import List, Tuple

from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
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

# Save the sub-sampled YCbCr image in the planar format (YUV420p)
height, width = images_data_as_ycbcr[0][0].shape
with open(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0-2_ycbcr.yuv420p.{width}x{height}.yuv",
    mode="wb",
) as images_ycbcr:
    for image_data_ycbcr in images_data_as_ycbcr:
        save_ycbcr_image(images_ycbcr, image_data_ycbcr)

##################
###  Analysis  ###
##################


def get_metrics_report(image_a: Image.Image, image_b: Image.Image) -> str:
    from pprint import pformat
    from numpy import Inf, int16
    from skimage.metrics import (
        mean_squared_error as get_mse,
        normalized_root_mse as get_nrmse,
        peak_signal_noise_ratio as get_psnr,
        structural_similarity as get_ssim,
    )

    image_copied_data = array(image_a, dtype=uint8)
    image_transformed_data = array(image_b, dtype=uint8)

    mae = abs(
        image_copied_data.astype(int16) - image_transformed_data.astype(int16)
    ).mean()
    mse = get_mse(image_copied_data, image_transformed_data)
    nrmse = get_nrmse(image_copied_data, image_transformed_data)
    if array_equal(image_copied_data, image_transformed_data):
        psnr = Inf
    else:
        psnr = get_psnr(image_copied_data, image_transformed_data)
    ssim = get_ssim(image_copied_data, image_transformed_data, channel_axis=-1)

    mae_best = 0.0
    mse_best = 0.0
    nrmse_best = 0.0
    psnr_best = Inf
    ssim_best = 1.0

    return f"""\
```python
{pformat(
    [
        ["<Metrics>", "<Score>", "<Goal>"],
        ["MAE", f"{mae:.5f}", f"{mae_best:.5f}"],
        ["MSE", f"{mse:.5f}", f"{mse_best:.5f}"],
        ["NRMSE", f"{nrmse:.5f}", f"{nrmse_best:.5f}"],
        ["PSNR", f"{psnr:.5f}", f"{psnr_best:.5f}"],
        ["SSIM", f"{ssim:.5f}", f"{ssim_best:.5f}"],
    ]
)}
```"""


print(
    """\
## Task 2

Convert the multiple images from RGB to YCbCr `4:2:0` color space
and pack them into a planar format.

### Comparison between the images with and without sub-sampling

The sub-sampled images are re-mapped from YCbCr to grayscale color space
for visualization purposes.

The up-sampled images are for comparison purposes.
"""
)
print(
    "".join(
        f"""\
The original image `{id}` in the RGB color space:

[![](../assets/foreman_qcif_{id}_rgb.bmp)](../assets/foreman_qcif_{id}_rgb.bmp)

The transformed image from `{id}` re-exported using `utils/YUVDisplay.exe`:

[![](./task_2/foreman_qcif_{id}_ycbcr.yuv420p.176x144.yuv.bmp)](./task_2/foreman_qcif_{id}_ycbcr.yuv420p.176x144.yuv.bmp)

The transformed images on different Y, Cb and Cr planes
from `{id}` in the grayscale colorspace:

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | [![](./task_2/foreman_qcif_{id}_y_without_subsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_y_without_subsampling.176x144.bmp)   | [![](./task_2/foreman_qcif_{id}_y_with_subsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_y_with_subsampling.176x144.bmp) | [![](./task_2/foreman_qcif_{id}_y_with_upsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_y_with_uppampling.176x144.bmp)   |
| On Cb plane | [![](./task_2/foreman_qcif_{id}_cb_without_subsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_cb_without_subsampling.176x144.bmp) | [![](./task_2/foreman_qcif_{id}_cb_with_subsampling.88x72.bmp)](./task_2/foreman_qcif_{id}_cb_with_subsampling.88x72.bmp)   | [![](./task_2/foreman_qcif_{id}_cb_with_upsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_cb_with_upsampling.176x144.bmp) |
| On Cr plane | [![](./task_2/foreman_qcif_{id}_cr_without_subsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_cr_without_subsampling.176x144.bmp) | [![](./task_2/foreman_qcif_{id}_cr_with_subsampling.88x72.bmp)](./task_2/foreman_qcif_{id}_cr_with_subsampling.88x72.bmp)   | [![](./task_2/foreman_qcif_{id}_cr_with_upsampling.176x144.bmp)](./task_2/foreman_qcif_{id}_cr_with_upsampling.176x144.bmp) |

"""
        for id in range(3)
    )
)
print(
    f"""\
Take the images with sequence number `3` to further comparison.

Below are the comparison metrics,
they are computed between the image without sub-sampling
and the other one with sub-sampling and up-sampling in the YCbCr color space:

The image pair on Y plane:

{get_metrics_report(image_y, image_y_upsampled)}

The image pair on Cb plane:

{get_metrics_report(image_cb, image_cb_upsampled)}

The image pair on Cr plane:

{get_metrics_report(image_cr, image_cr_upsampled)}
"""
)
print(
    """\
### Details

The workflow is as follows:

```mermaid
graph LR
    drgb[/Digital RGB Image 0~255/]
    argb([Analog RGB Image 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr Image 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr Image 16~235; 16~240/]
    sub[Sub-sampling 4:2:0]
    ups[Up-sampling from 4:2:0 to 4:4:4]
    pack[Pack YCbCr frames in YUV420p format]

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
