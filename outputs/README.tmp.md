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

I added transformed images from YCbCr to RGB using `utils/YUVDisplay.exe`.

There are the images in the RGB color space below.

| Copied Image | Transformed Image (Mine) | Transformed Image (YUVDisplay.exe) |
| ------------ | ------------------------ | ---------------------------------- |
| ![](./task_1/foreman_qcif_0_rgb_copied.176x144.bmp) | ![](./task_1/foreman_qcif_0_rgb_transformed.176x144.bmp) | ![](./task_1/foreman_qcif_0_ycbcr.yuv420p.176x144.yuv.bmp) |

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

```mermaid
graph LR
    drgb[/Digital RGB image 0~255/]
    argb([Analog RGB image 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr image 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr image 16~235; 16~240/]
    sub[Sub-sampling to 4:2:0]
    ups[Up-sampling from 4:2:0 to 4:4:4]

    drgb -->|1| argb
    argb -->|2| tran
    tran -->|3| ayuv
    ayuv -->|4| dyuv
    dyuv -->|5| sub
    sub -->|6| ups
    ups -->|7| dyuv
    dyuv -->|8| ayuv
    ayuv -->|9| tran
    tran -->|10| argb
    argb -->|11| drgb
```

## Task 2

Convert the multiple images from RGB to YCbCr `4:2:0` color space
and pack them into a file in planar format.

### Visual Comparison

Display images.

I added the up-sampled images and re-exported them using `utils/YUVDisplay.exe`
for comparison purposes since they have the same size as the original ones.

The images with sequence number `0` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_0_rgb.bmp) | ![](./task_2/foreman_qcif_0_ycbcr.yuv420p.176x144.yuv.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_0_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_0_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_0_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_0_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_0_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_0_cr_with_upsampling.176x144.bmp) |
The images with sequence number `1` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_1_rgb.bmp) | ![](./task_2/foreman_qcif_1_ycbcr.yuv420p.176x144.yuv.bmp) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_1_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_1_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_1_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_1_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_1_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_1_cr_with_upsampling.176x144.bmp) |
The images with sequence number `2` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_2_rgb.bmp) | ![](./task_2/foreman_qcif_2_ycbcr.yuv420p.176x144.yuv.bmp) |

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

```mermaid
graph LR
    drgb[/Digital RGB images 0~255/]
    argb([Analog RGB images 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr images 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr images 16~235; 16~240/]
    sub[Sub-sampling to 4:2:0]
    ups[Up-sampling from 4:2:0 to 4:4:4]
    pack[Pack YCbCr images in YUV420p format]

    drgb -->|1| argb
    argb -->|2| tran
    tran -->|3| ayuv
    ayuv -->|4| dyuv
    dyuv -->|5| sub
    sub -->|6| pack
    sub -->|7| ups
    ups -->|8| dyuv
```

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

```mermaid
graph TD
    114048 --> 46189
    114048 --> 67859
    46189 --> 21124
    46189 --> 25065:7
    21124 --> 9342
    21124 --> 11782
    9342 --> 4350
    9342 --> 4992:12
    4350 --> 2127:11
    4350 --> 2223:10
    2127:11
    2223:10
    4992:12
    11782 --> 5697:9
    11782 --> 6085:15
    5697:9
    6085:15
    25065:7
    67859 --> 29119
    67859 --> 38740
    29119 --> 13400
    29119 --> 15719:13
    13400 --> 6675
    13400 --> 6725:5
    6675 --> 2444
    6675 --> 4231:4
    2444 --> 1010
    2444 --> 1434:3
    1010 --> 437
    1010 --> 573:2
    437 --> 32:1
    437 --> 405:0
    32:1
    405:0
    573:2
    1434:3
    4231:4
    6725:5
    15719:13
    38740 --> 17626
    38740 --> 21114:8
    17626 --> 8314:6
    17626 --> 9312:14
    8314:6
    9312:14
    21114:8

```

I added assertion checks to ensure that
the decoded images are equal to the quantized images.
(See the module `src.tasks.quantize_and_encode_multi_frame_in_ycbcr420_and_back`)

I added the re-exported images using `utils/YUVDisplay.exe`
for comparison purposes since they have the same size as the original ones.

The images with sequence number `0` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_0_rgb.bmp) | ![](#) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_0_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_0_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_0_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_0_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_0_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_0_cr_dequantized.88x72.bmp)  |
The images with sequence number `1` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_1_rgb.bmp) | ![](#) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_1_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_1_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_1_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_1_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_1_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_1_cr_dequantized.88x72.bmp)  |
The images with sequence number `2` are displayed below.

There are the images in the RGB color space below.

| Original Image | Transformed Image (YUVDisplay.exe) |
| -------------- | ---------------------------------- |
| ![](./assets/foreman_qcif_2_rgb.bmp) | ![](#) |

There are images in the YCbCr color space re-mapped to the grayscale color space below.

|             | Before quantized | After de-quantized |
| ----------- | ---------------- | ------------------ |
| On Y plane  | ![](./task_3/foreman_qcif_2_y_before_quantized.176x144.bmp) | ![](./task_3/foreman_qcif_2_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_3/foreman_qcif_2_cb_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_2_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_3/foreman_qcif_2_cr_before_quantized.88x72.bmp)  | ![](./task_3/foreman_qcif_2_cr_dequantized.88x72.bmp)  |

### Details

The process workflow is as follows.

```mermaid
graph LR
    dyuv[/Digital YCbCr images 16~235; 16~240/]
    sub[Sub-sampling to 4:2:0]
    qua[Quantization in 16 levels from 16~240]
    enc[Encoding using Huffman coding]
    bun[Bundle the encoded images with metadata]
    ubu[Un-bundle the encoded images with metadata]
    dec[Decoding using Huffman coding]
    dqu[De-quantization in 16 levels to 16~240]
    ups[Up-sampling from 4:2:0 to 4:4:4]

    dyuv -->|1| sub
    sub -->|2| qua
    qua -->|3| enc
    enc -->|4| bun
    bun -->|5| ubu
    ubu -->|6| dec
    dec -->|7| dqu
    dqu -->|8| ups
    ups -->|9| dyuv
```

