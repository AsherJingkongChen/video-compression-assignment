from PIL import Image
from numpy import array, uint8
from .utils.env import ASSETS_DIR_PATH, OUTPUTS_DIR_PATH
from ..modules.color import H273, KR_KB_BT601
from ..modules.data import (
    packed_from_planar,
    planar_from_packed,
    save_ycbcr_image,
)
from ..modules.sample import BT2100

OUTPUTS_DIR_PATH = OUTPUTS_DIR_PATH / "task_2"
OUTPUTS_DIR_PATH.mkdir(parents=True, exist_ok=True)

# Open the output file
frames = open(OUTPUTS_DIR_PATH / "foreman_qcif_0-2_ycbcr.yuv420p.176x144.yuv", "wb")

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

    # Write the sub-sampled YCbCr image in the planar format (YUV420p)
    save_ycbcr_image(
        frames,
        (
            image_data_as_y_subsampled,
            image_data_as_cb_subsampled,
            image_data_as_cr_subsampled,
        ),
    )

##################
###  Analysis  ###
##################

# from pprint import pprint
# from numpy import Inf, int16
# from skimage.metrics import (
#     mean_squared_error as get_mse,
#     normalized_root_mse as get_nrmse,
#     peak_signal_noise_ratio as get_psnr,
#     structural_similarity as get_ssim,
# )

# image_copied_data = array(image_copied, dtype=uint8)
# image_transformed_data = array(image_transformed, dtype=uint8)

# mae = abs(image_copied_data.astype(int16) - image_transformed_data.astype(int16)).mean()
# mse = get_mse(image_copied_data, image_transformed_data)
# nrmse = get_nrmse(image_copied_data, image_transformed_data)
# psnr = get_psnr(image_copied_data, image_transformed_data)
# ssim = get_ssim(image_copied_data, image_transformed_data, channel_axis=-1)

# mae_best = 0.0
# mse_best = 0.0
# nrmse_best = 0.0
# psnr_best = Inf
# ssim_best = 1.0
# xae_best = 0.0

# # Show the metrics
# pprint(
#     [
#         ["<Metrics>", "<Score>", "<Maximum>"],
#         ["MAE", f"{mae:.5f}", f"{mae_best:.5f}"],
#         ["MSE", f"{mse:.5f}", f"{mse_best:.5f}"],
#         ["NRMSE", f"{nrmse:.5f}", f"{nrmse_best:.5f}"],
#         ["PSNR", f"{psnr:.5f}", f"{psnr_best:.5f}"],
#         ["SSIM", f"{ssim:.5f}", f"{ssim_best:.5f}"],
#     ]
# )
