from PIL import Image
from numpy import array, uint8
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601
from ..modules.data import (
    packed_from_planar,
    planar_from_packed,
    save_ycbcr_image,
)
from ..modules.sample import BT2100, SUBSAMPLING_SCHEME_420

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

##################
###  Analysis  ###
##################

from pprint import pprint
from numpy import Inf, int16
from skimage.metrics import (
    mean_squared_error as get_mse,
    normalized_root_mse as get_nrmse,
    peak_signal_noise_ratio as get_psnr,
    structural_similarity as get_ssim,
)

image_copied_data = array(image_copied, dtype=uint8)
image_transformed_data = array(image_transformed, dtype=uint8)

mae = abs(image_copied_data.astype(int16) - image_transformed_data.astype(int16)).mean()
mse = get_mse(image_copied_data, image_transformed_data)
nrmse = get_nrmse(image_copied_data, image_transformed_data)
psnr = get_psnr(image_copied_data, image_transformed_data)
ssim = get_ssim(image_copied_data, image_transformed_data, channel_axis=-1)

mae_best = 0.0
mse_best = 0.0
nrmse_best = 0.0
psnr_best = Inf
ssim_best = 1.0

# Show the metrics
print(
    """\
# Assignment 1 code outputs

## Task 1

Convert an image from RGB to YCbCr 4:2:0 and recover it.

Below are the metrics to compare
the copied and transformed images in the RGB color space:

```python"""
)
pprint(
    [
        ["<Metrics>", "<Score>", "<Goal>"],
        ["MAE", f"{mae:.5f}", f"{mae_best:.5f}"],
        ["MSE", f"{mse:.5f}", f"{mse_best:.5f}"],
        ["NRMSE", f"{nrmse:.5f}", f"{nrmse_best:.5f}"],
        ["PSNR", f"{psnr:.5f}", f"{psnr_best:.5f}"],
        ["SSIM", f"{ssim:.5f}", f"{ssim_best:.5f}"],
    ]
)
print("```")
