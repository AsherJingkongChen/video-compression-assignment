from PIL import Image
from pathlib import Path
from numpy import array, uint8

ASSETS_DIR_PATH = (Path(__file__) / "../../../assets").resolve()
OUTPUTS_DIR_PATH = (Path(__file__) / "../../../outputs").resolve()
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# The source image's bits per pixel is 32 (RGB with 1-byte padding)
source_image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp").convert("RGBX")
shape = (source_image.height, source_image.width, source_image.getbands().__len__())
source_data = array(source_image.getdata(), dtype=uint8).reshape(shape)

print(source_data)
print(source_data.shape)

target_image = Image.fromarray(source_data)
target_image.save(OUTPUTS_DIR_PATH / "foreman_qcif_0_rgb_copy.bmp")
