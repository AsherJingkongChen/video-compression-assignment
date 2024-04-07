from PIL import Image
from numpy import array, uint8
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601

image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp").convert("RGB")
image_data_as_drgb = array(image, dtype=uint8)

# Ensure that the source image is in the full range RGB color space

image_must_be_full_range = (image_data_as_drgb.max() > 219 + 16) or (
    image_data_as_drgb.min() < 16
)
assert (
    image_must_be_full_range
), "The source image is assumed to be in the full range RGB color space"

# Uses ITU-R BT.601 parameter values
color = H273()

# De-quanitze the image
color.set_full_range(True)
image_data_as_argb = color.dequantize_rgb(image_data_as_drgb)

# Convert the image from analog RGB to YPbPr
color.set_rgb_gamma_corrected(True)
kr, kb = KR_KB_BT601()
image_data_as_ypbpr = color.ypbpr_from_rgb(image_data_as_argb, kr, kb)

# Quantize the image from YPbPr to YCbCr
color.set_full_range(False)
image_data_as_ycbcr = color.quantize_ypbpr(image_data_as_ypbpr)

# Convert the image from YPbPr to analog RGB
image_data_as_argb = color.rgb_from_ypbpr(image_data_as_ypbpr, kr, kb)

# Quantize the image from analog RGB to digital RGB
color.set_full_range(True)
image_data_as_drgb_remade = color.quantize_rgb(image_data_as_argb)

print(image_data_as_drgb.size)
print(image_data_as_drgb.reshape(-1, 3))
print(image_data_as_drgb_remade.reshape(-1, 3))
print((image_data_as_drgb.astype(int) - image_data_as_drgb_remade.astype(int)).mean())
