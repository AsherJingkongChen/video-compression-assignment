from PIL import Image
from numpy import array, all, uint8
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601

image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp").convert("RGB")
image_data = array(image, dtype=uint8)

# Ensure that the source image is in the full range RGB color space

image_must_be_full_range = (image_data.max() > 219 + 16) or (
    image_data.min() < 16
)
assert image_must_be_full_range, "Source image are assumed to be in the full range RGB color space"

# Uses ITU-R BT.601 parameter values
rec = H273()

# De-quanitze the source image
rec.set_full_range(True)
image_data_as_argb = rec.dequantize_rgb(image_data)

# Convert the source image from analog RGB to YPbPr
rec.set_rgb_gamma_corrected(True)
kr, kb = KR_KB_BT601()
image_data_as_ypbpr = rec.ypbpr_from_rgb(image_data_as_argb, kr, kb)

# Quantize the source image from YPbPr to YCbCr
rec.set_full_range(False)
image_data_as_ycbcr = rec.quantize_ypbpr(image_data_as_ypbpr)

image_data_as_ypbpr = rec.dequantize_ycbcr(image_data_as_ycbcr)

image_data_as_argb = rec.rgb_from_ypbpr(image_data_as_ypbpr, kr, kb)

rec.set_full_range(True)
image_data_back = rec.quantize_rgb(image_data_as_argb)

print(image_data.size)
print((image_data.astype(int) - image_data_back.astype(int)).mean())