# Assignment 1 Code Outputs

## Reproduction

1. Install the requirements

    ```shell
    python3 -m pip install -Ur requirements.txt
    ```

2. Run all the tasks

    ```shell
    python3 run_tasks.py
    ```

## Task 1

Convert an image from RGB to YCbCr `4:2:0` and recover it.

*Assume that the copied image is equivalent to the original image.*

### Visual Comparison

Display images.

There are the images in the RGB color space below.

| Copied Image | Transformed Image |
| ------------ | ----------------- |
| ![](./task_1/foreman_qcif_0_rgb_copied.176x144.bmp) | ![](./task_1/foreman_qcif_0_rgb_transformed.176x144.bmp) |

There are the images in the YCbCr color space re-mapped to the grayscale colorspace below.

|             | Before sub-sampling | After sub-sampling | After up-sampling |
| ----------- | ------------------- | ------------------ | ----------------- |
| On Y plane  | ![](./task_1/foreman_qcif_0_y_default.176x144.bmp)  | ![](./task_1/foreman_qcif_0_y_subsampled.176x144.bmp) | ![](./task_1/foreman_qcif_0_y_upsampled.176x144.bmp)  |
| On Cb plane | ![](./task_1/foreman_qcif_0_cb_default.176x144.bmp) | ![](./task_1/foreman_qcif_0_cb_subsampled.88x72.bmp)  | ![](./task_1/foreman_qcif_0_cb_upsampled.176x144.bmp) |
| On Cr plane | ![](./task_1/foreman_qcif_0_cr_default.176x144.bmp) | ![](./task_1/foreman_qcif_0_cr_subsampled.88x72.bmp)  | ![](./task_1/foreman_qcif_0_cr_upsampled.176x144.bmp) |

### Statistical Comparison

Compare between the copied and transformed images in the RGB color space.

There are the metric results computed
between the copied and transformed images below.

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.48102', '0.00000'],
 ['MSE', '0.73883', '0.00000'],
 ['NRMSE', '0.00483', '0.00000'],
 ['PSNR', '49.44534', 'inf'],
 ['SSIM', '0.99853', '1.00000']]
```

### Details

The process workflow is as follows.

![diagram](./README-1.svg)

## Task 2

Convert the multiple images from RGB to YCbCr `4:2:0` color space
and pack them into a file in planar format.

### Visual Comparison

Display images.

I added the up-sampled images for comparison purposes
since they have the same size as the original ones.

The images with sequence number `0` are displayed below.

There are the images in the RGB color space below.

| Copied Image | Transformed Image |
| ------------ | ----------------- |
| ![](./task_2/foreman_qcif_0_rgb_copied.176x144.bmp) | ![](./task_2/foreman_qcif_0_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_0_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_0_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_0_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_0_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_0_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_0_cr_with_upsampling.176x144.bmp) |

The images with sequence number `1` are displayed below.

There are the images in the RGB color space below.

| Copied Image | Transformed Image |
| ------------ | ----------------- |
| ![](./task_2/foreman_qcif_1_rgb_copied.176x144.bmp) | ![](./task_2/foreman_qcif_1_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_1_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_1_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_1_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_1_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_1_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_1_cr_with_upsampling.176x144.bmp) |

The images with sequence number `2` are displayed below.

There are the images in the RGB color space below.

| Copied Image | Transformed Image |
| ------------ | ----------------- |
| ![](./task_2/foreman_qcif_2_rgb_copied.176x144.bmp) | ![](./task_2/foreman_qcif_2_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_2_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_2_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_2_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_2_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_2_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_2_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_2_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_2_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_2_cr_with_upsampling.176x144.bmp) |

### Statistical Comparison

Compare between the images without sub-sampling and with sub-sampling
in the YCbCr color space.

There are the metric results computed
between the copied and transformed images below.

The image pair with sequence number `0`:

On the Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.00000', '0.00000'],
 ['MSE', '0.00000', '0.00000'],
 ['NRMSE', '0.00000', '0.00000'],
 ['PSNR', 'inf', 'inf'],
 ['SSIM', '1.00000', '1.00000']]
```

On the Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.01610', '0.00000'],
 ['MSE', '0.04553', '0.00000'],
 ['NRMSE', '0.00179', '0.00000'],
 ['PSNR', '61.54750', 'inf'],
 ['SSIM', '0.99981', '1.00000']]
```

On the Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.02233', '0.00000'],
 ['MSE', '0.22230', '0.00000'],
 ['NRMSE', '0.00350', '0.00000'],
 ['PSNR', '54.66139', 'inf'],
 ['SSIM', '0.99976', '1.00000']]
```

The image pair with sequence number `1`:

On the Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.00000', '0.00000'],
 ['MSE', '0.00000', '0.00000'],
 ['NRMSE', '0.00000', '0.00000'],
 ['PSNR', 'inf', 'inf'],
 ['SSIM', '1.00000', '1.00000']]
```

On the Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.01172', '0.00000'],
 ['MSE', '0.04076', '0.00000'],
 ['NRMSE', '0.00169', '0.00000'],
 ['PSNR', '62.02855', 'inf'],
 ['SSIM', '0.99988', '1.00000']]
```

On the Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.02225', '0.00000'],
 ['MSE', '0.21607', '0.00000'],
 ['NRMSE', '0.00345', '0.00000'],
 ['PSNR', '54.78492', 'inf'],
 ['SSIM', '0.99980', '1.00000']]
```

The image pair with sequence number `2`:

On the Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.00000', '0.00000'],
 ['MSE', '0.00000', '0.00000'],
 ['NRMSE', '0.00000', '0.00000'],
 ['PSNR', 'inf', 'inf'],
 ['SSIM', '1.00000', '1.00000']]
```

On the Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.01417', '0.00000'],
 ['MSE', '0.04257', '0.00000'],
 ['NRMSE', '0.00173', '0.00000'],
 ['PSNR', '61.83934', 'inf'],
 ['SSIM', '0.99984', '1.00000']]
```

On the Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.02095', '0.00000'],
 ['MSE', '0.21784', '0.00000'],
 ['NRMSE', '0.00346', '0.00000'],
 ['PSNR', '54.74938', 'inf'],
 ['SSIM', '0.99982', '1.00000']]
```

### Details

The process workflow is as follows.

![diagram](./README-2.svg)

## Task 3

Quantize in 16 levels and encode YCbCr `4:2:0` images and recover them.

Uses Huffman coding scheme.

### Visual Comparison

Display structures and images.

There are 16 symbols in Huffman code table as the number of quantization levels.

There are the code table and tree diagram of the Huffman tree used below.

```python
{0: '10000001',
 1: '10000000',
 2: '1000001',
 3: '100001',
 4: '10001',
 5: '1001',
 6: '1100',
 7: '01',
 8: '111',
 9: '0010',
 10: '00001',
 11: '00000',
 12: '0001',
 13: '101',
 14: '1101',
 15: '0011'}
```

![diagram](./README-3.svg)

I added assertion checks to ensure that
the decoded images are equal to the quantized images.
(See the module `src.tasks.quantize_and_encode_multi_frame_in_ycbcr420_and_back`)

I added the up-sampled images for comparison purposes
since they have the same size as the original ones.

The images with sequence number `0` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image |
| -------------- | ----------------- |
| ![](../assets/foreman_qcif_0_rgb.bmp) | ![](./task_3/foreman_qcif_0_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_0_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_0_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_0_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_0_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_0_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_0_cr_dequantized.88x72.bmp)  |

The images with sequence number `1` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image |
| -------------- | ----------------- |
| ![](../assets/foreman_qcif_1_rgb.bmp) | ![](./task_3/foreman_qcif_1_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_1_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_1_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_1_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_1_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_1_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_1_cr_dequantized.88x72.bmp)  |

The images with sequence number `2` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image |
| -------------- | ----------------- |
| ![](../assets/foreman_qcif_2_rgb.bmp) | ![](./task_3/foreman_qcif_2_rgb_transformed.176x144.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_2_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_2_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_2_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_2_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_2_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_2_cr_dequantized.88x72.bmp)  |

### Statistical Comparison

The image pair with sequence number `0`:

On the Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '7.39583', '0.00000'],
 ['MSE', '68.90554', '0.00000'],
 ['NRMSE', '0.04882', '0.00000'],
 ['PSNR', '29.74826', 'inf'],
 ['SSIM', '0.93219', '1.00000']]
```

On the Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '6.20739', '0.00000'],
 ['MSE', '54.14331', '0.00000'],
 ['NRMSE', '0.06166', '0.00000'],
 ['PSNR', '30.79536', 'inf'],
 ['SSIM', '0.91321', '1.00000']]
```

On the Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '5.69776', '0.00000'],
 ['MSE', '48.57812', '0.00000'],
 ['NRMSE', '0.05172', '0.00000'],
 ['PSNR', '31.26640', 'inf'],
 ['SSIM', '0.92156', '1.00000']]
```

The image pair with sequence number `1`:

On the Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '7.42551', '0.00000'],
 ['MSE', '69.23674', '0.00000'],
 ['NRMSE', '0.04901', '0.00000'],
 ['PSNR', '29.72744', 'inf'],
 ['SSIM', '0.93298', '1.00000']]
```

On the Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '6.22617', '0.00000'],
 ['MSE', '54.61695', '0.00000'],
 ['NRMSE', '0.06194', '0.00000'],
 ['PSNR', '30.75753', 'inf'],
 ['SSIM', '0.91339', '1.00000']]
```

On the Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '5.70849', '0.00000'],
 ['MSE', '48.54467', '0.00000'],
 ['NRMSE', '0.05167', '0.00000'],
 ['PSNR', '31.26939', 'inf'],
 ['SSIM', '0.92171', '1.00000']]
```

The image pair with sequence number `2`:

On the Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '7.41020', '0.00000'],
 ['MSE', '69.00994', '0.00000'],
 ['NRMSE', '0.04898', '0.00000'],
 ['PSNR', '29.74169', 'inf'],
 ['SSIM', '0.93281', '1.00000']]
```

On the Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '6.23658', '0.00000'],
 ['MSE', '55.15199', '0.00000'],
 ['NRMSE', '0.06224', '0.00000'],
 ['PSNR', '30.71519', 'inf'],
 ['SSIM', '0.90988', '1.00000']]
```

On the Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '5.77383', '0.00000'],
 ['MSE', '49.73122', '0.00000'],
 ['NRMSE', '0.05226', '0.00000'],
 ['PSNR', '31.16451', 'inf'],
 ['SSIM', '0.92437', '1.00000']]
```

### Details

The process workflow is as follows.

![diagram](./README-4.svg)

