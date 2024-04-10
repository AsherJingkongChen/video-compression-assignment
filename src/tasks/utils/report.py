from PIL.Image import Image


def get_metrics_report(image_a: Image, image_b: Image) -> str:
    from pprint import pformat
    from numpy import array, array_equal, Inf, uint8, int16
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
    psnr = Inf
    if not array_equal(image_copied_data, image_transformed_data):
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
