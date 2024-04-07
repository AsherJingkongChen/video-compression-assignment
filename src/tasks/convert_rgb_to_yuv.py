from PIL import Image
from pathlib import Path
from numpy import array, all

from ..modules.color import H273, KR_KB_BT601, KR_KB_BT709

ASSETS_DIR_PATH = (Path(__file__) / "../../../assets").resolve()
OUTPUTS_DIR_PATH = (Path(__file__) / "../../../outputs").resolve()
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# The source image's bits per pixel is 32 (RGB with 1-byte padding)
source_image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_2_rgb.bmp").convert("RGB")
source_data = array(source_image)

h273 = H273()
print(source_data.shape)
dequant_data = h273.set_full_range(True).dequantize_rgb(source_data)
quant_data = h273.set_full_range(True).quantize_rgb(dequant_data)
print(all(source_data == quant_data))

# trmat = H273().get_ypbpr_transformation_matrix(*KR_KB_BT601())
# print(trmat)
# trmat = H273().get_ypbpr_transformation_matrix(*KR_KB_BT709())
# print(trmat)


# target_image = YUVImage.from_pil_image(source_image)
# source_image.convert("L").save(OUTPUTS_DIR_PATH / "foreman_qcif_0_l.bmp")
# Image.fromarray(target_image.y_plane, mode="L").save(
#     OUTPUTS_DIR_PATH / "foreman_qcif_0_y.bmp"
# )
# print(target_image)

# target_image = Image.fromarray(source_data)
# target_image.save(OUTPUTS_DIR_PATH / "foreman_qcif_0_rgb_copy.bmp")
