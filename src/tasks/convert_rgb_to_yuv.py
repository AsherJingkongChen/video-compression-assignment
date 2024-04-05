from PIL import Image
from pathlib import Path

from ..modules.image import YUVImage

ASSETS_DIR_PATH = (Path(__file__) / "../../../assets").resolve()
OUTPUTS_DIR_PATH = (Path(__file__) / "../../../outputs").resolve()
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# The source image's bits per pixel is 32 (RGB with 1-byte padding)
source_image = Image.open(ASSETS_DIR_PATH / "foreman_qcif_0_rgb.bmp").convert("RGB")
target_image = YUVImage.from_pil_image(source_image)
source_image.convert("L").save(OUTPUTS_DIR_PATH / "foreman_qcif_0_l.bmp")
Image.fromarray(target_image.y_plane, mode="L").save(
    OUTPUTS_DIR_PATH / "foreman_qcif_0_y.bmp"
)
print(target_image)

# target_image = Image.fromarray(source_data)
# target_image.save(OUTPUTS_DIR_PATH / "foreman_qcif_0_rgb_copy.bmp")
