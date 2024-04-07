from PIL import Image
from numpy import array, uint8, int32
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601
from ..modules.data import (
    packed_from_planar,
    planar_from_packed,
    save_ycbcr_image,
)
from ..modules.sample import BT2100

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

# Uses ITU-R BT.601 parameter values
# - The source image is assumed to be gamma-corrected RGB
color = H273()

# Uses ITU-R BT.2100 parameter values
# - The sub-sampling methods are easier to implement
sample = BT2100()

# De-quanitze the image from digital RGB to analog RGB
image_data_as_argb = color.set_full_range(True).dequantize_rgb(image_data_as_drgb)

# Convert the image from analog RGB to YPbPr
kr, kb = KR_KB_BT601()
image_data_as_ypbpr = color.ypbpr_from_rgb(image_data_as_argb, kr, kb)

# Quantize the image from YPbPr to YCbCr
image_data_as_ycbcr = color.set_full_range(False).quantize_ycbcr(image_data_as_ypbpr)

# Sub-sample the image in YCbCr color space using 4:2:0 scheme
image_data_as_y, image_data_as_cb, image_data_as_cr = planar_from_packed(
    image_data_as_ycbcr
)
image_data_as_y_subsampled = image_data_as_y.copy()
image_data_as_cb_subsampled = sample.subsample_420(
    image_data_as_y,
    image_data_as_cb,
)
image_data_as_cr_subsampled = sample.subsample_420(
    image_data_as_y,
    image_data_as_cr,
)

# Save the sub-sampled image in the planar YCbCr format a.k.a. YUV420p
height, width = image_data_as_y_subsampled.shape
with open(
    OUTPUTS_DIR_PATH / f"foreman_qcif_0_ycbcr.yuv420p.{width}x{height}.yuv",
    mode="wb",
) as file:
    save_ycbcr_image(
        file,
        (
            image_data_as_y_subsampled,
            image_data_as_cb_subsampled,
            image_data_as_cr_subsampled,
        ),
    )

# Up-sample the image in YCbCr color space from 4:2:0 to 4:4:4 scheme
image_data_as_y_upsampled = image_data_as_y_subsampled.copy()
image_data_as_cb_upsampled = sample.upsample_420(
    image_data_as_y_subsampled,
    image_data_as_cb_subsampled,
)
image_data_as_cr_upsampled = sample.upsample_420(
    image_data_as_y_subsampled,
    image_data_as_cr_subsampled,
)
image_data_as_ycbcr_upsampled = packed_from_planar((
    image_data_as_y_upsampled,
    image_data_as_cb_upsampled,
    image_data_as_cr_upsampled,
))

# De-quantize the image from YCbCr to YPbPr
image_data_as_ypbpr_back = color.set_full_range(False).dequantize_ycbcr(
    image_data_as_ycbcr_upsampled
)

# Convert the image from YPbPr to analog RGB
image_data_as_argb_back = color.rgb_from_ypbpr(image_data_as_ypbpr_back, kr, kb)

# Quantize the image from analog RGB to digital RGB
image_data_as_drgb_back = color.set_full_range(True).quantize_rgb(
    image_data_as_argb_back
)

# Save the image in the 24-bit RGB BMP format
image_back = Image.fromarray(image_data_as_drgb_back, mode="RGB")
width, height = image_back.size
image_back.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_rgb.{width}x{height}.bmp")

# Ensure that the back image has the same size as the source image
assert (
    image.size == image_back.size
), "The back image should have the same size as the source image"

a = image_data_as_drgb.astype(int32)
b = image_data_as_drgb_back.astype(int32)
r = abs(a - b).max()
me = (a - b).mean()
mse = ((a - b) ** 2).mean()
print(f"R: {r}, ME: {me:.3f}, MSE: {mse:.3f}")
