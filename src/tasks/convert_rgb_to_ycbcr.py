from PIL import Image
from numpy import array, moveaxis, uint8
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601

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
color = H273(rgb_gamma_corrected=True)

# De-quanitze the image to analog RGB
image_data_as_argb = color.set_full_range(True).dequantize_rgb(image_data_as_drgb)

# Convert the image from analog RGB to YPbPr
kr, kb = KR_KB_BT601()
image_data_as_ypbpr = color.ypbpr_from_rgb(image_data_as_argb, kr, kb)

image_data_as_ycbcr = color.set_full_range(False).quantize_ypbpr(image_data_as_ypbpr)

# Quantize the image from YPbPr to YCbCr
print(image_data_as_ycbcr.min(), image_data_as_ycbcr.max())

planar_image_data = moveaxis(image_data_as_ycbcr, -1, 0)
y_plane, cb_plane, cr_plane = planar_image_data
cb_plane = cb_plane[::2, ::2]
cr_plane = cr_plane[::2, ::2]
planar_image_data_as_bytes = y_plane.tobytes() + cb_plane.tobytes() + cr_plane.tobytes()
height, width = y_plane.shape
(OUTPUTS_DIR_PATH / f"foreman_qcif_0_ycbcr.{width}x{height}.yuv").write_bytes(
    planar_image_data_as_bytes
)

# Sub-sample the image in YPbPr color space using 4:2:0 scheme
pass

# Save the sub-sampled image in the planar format
pass

# Up-sample the image in YPbPr color space using 4:2:0 scheme
pass

# Convert the image from YPbPr to analog RGB
image_data_as_argb_back = color.rgb_from_ypbpr(image_data_as_ypbpr, kr, kb)

# Quantize the image from analog RGB to digital RGB
image_data_as_drgb_back = color.set_full_range(True).quantize_rgb(
    image_data_as_argb_back
)

# Save the image in the 24-bit RGB BMP format
image_back = Image.fromarray(image_data_as_drgb_back, mode="RGB")
width, height = image_back.size
image_back.save(OUTPUTS_DIR_PATH / f"foreman_qcif_0_rgb_back.{width}x{height}.bmp")

# Ensure that the back image has the same size as the source image
assert (
    image.size == image_back.size
), "The back image should have the same size as the source image"
