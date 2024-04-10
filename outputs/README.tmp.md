# Assignment 1 Code Outputs

## Task 1

Convert an image from RGB to YCbCr `4:2:0` and recover it.

*Assume that the copied image is equivalent to the original image.*

### Statistical Comparison

Compare between the copied and transformed images in the RGB color space.

There are the metric results computed
between the copied and transformed images below:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.48102', '0.00000'],
 ['MSE', '0.73883', '0.00000'],
 ['NRMSE', '0.00483', '0.00000'],
 ['PSNR', '49.44534', 'inf'],
 ['SSIM', '0.99853', '1.00000']]
```

### Visual Comparison

Display images.

There are the images in the RGB color space below; by the way,
I add transformed images from YCbCr to RGB using `utils/YUVDisplay.exe`:

| Copied Image | Transformed Image (Mine) | Transformed Image (YUVDisplay.exe) |
| ------------ | ------------------------ | ---------------------------------- |
| ![](./task_1/foreman_qcif_0_rgb_copied.176x144.bmp) | ![](./task_1/foreman_qcif_0_rgb_transformed.176x144.bmp) | ![](./task_1/foreman_qcif_0_ycbcr.yuv420p.176x144.yuv.bmp) |

There are the images in the YCbCr color space re-mapped in the grayscale colorspace:

|             | Before sub-sampling | After sub-sampling | After up-sampling |
| ----------- | ------------------- | ------------------ | ----------------- |
| On Y plane  | ![](./task_1/foreman_qcif_0_y_default.176x144.bmp)  | ![](./task_1/foreman_qcif_0_y_subsampled.176x144.bmp) | ![](./task_1/foreman_qcif_0_y_upsampled.176x144.bmp)  |
| On Cb plane | ![](./task_1/foreman_qcif_0_cb_default.176x144.bmp) | ![](./task_1/foreman_qcif_0_cb_subsampled.88x72.bmp)  | ![](./task_1/foreman_qcif_0_cb_upsampled.176x144.bmp) |
| On Cr plane | ![](./task_1/foreman_qcif_0_cr_default.176x144.bmp) | ![](./task_1/foreman_qcif_0_cr_subsampled.88x72.bmp)  | ![](./task_1/foreman_qcif_0_cr_upsampled.176x144.bmp) |

### Details

The workflow is as follows:

```mermaid
graph LR
    drgb[/Digital RGB Image 0~255/]
    argb([Analog RGB Image 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr Image 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr Image 16~235; 16~240/]
    sub[Sub-sampling 4:2:0]
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
and pack them into a planar format.

### Comparison between the images with and without sub-sampling

The sub-sampled images are re-mapped from YCbCr to grayscale color space
for visualization purposes.

The up-sampled images are for comparison purposes.

The original image `0` in the RGB color space:

![](../assets/foreman_qcif_0_rgb.bmp)

The transformed image from `0` re-exported using `utils/YUVDisplay.exe`:

![](./task_2/foreman_qcif_0_ycbcr.yuv420p.176x144.yuv.bmp)

The transformed images on different Y, Cb and Cr planes
from `0` in the grayscale colorspace:

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_0_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_0_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_0_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_0_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_0_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_0_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_0_cr_with_upsampling.176x144.bmp) |

The original image `1` in the RGB color space:

![](../assets/foreman_qcif_1_rgb.bmp)

The transformed image from `1` re-exported using `utils/YUVDisplay.exe`:

![](./task_2/foreman_qcif_1_ycbcr.yuv420p.176x144.yuv.bmp)

The transformed images on different Y, Cb and Cr planes
from `1` in the grayscale colorspace:

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_1_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_1_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_1_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_1_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_1_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_1_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_1_cr_with_upsampling.176x144.bmp) |

The original image `2` in the RGB color space:

![](../assets/foreman_qcif_2_rgb.bmp)

The transformed image from `2` re-exported using `utils/YUVDisplay.exe`:

![](./task_2/foreman_qcif_2_ycbcr.yuv420p.176x144.yuv.bmp)

The transformed images on different Y, Cb and Cr planes
from `2` in the grayscale colorspace:

|             | Without sub-sampling | With sub-sampling | With up-sampling |
| ----------- | -------------------- | ----------------- | ---------------- |
| On Y plane  | ![](./task_2/foreman_qcif_2_y_without_subsampling.176x144.bmp)  | ![](./task_2/foreman_qcif_2_y_with_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_2_y_with_upsampling.176x144.bmp)  |
| On Cb plane | ![](./task_2/foreman_qcif_2_cb_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_2_cb_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_2_cb_with_upsampling.176x144.bmp) |
| On Cr plane | ![](./task_2/foreman_qcif_2_cr_without_subsampling.176x144.bmp) | ![](./task_2/foreman_qcif_2_cr_with_subsampling.88x72.bmp)  | ![](./task_2/foreman_qcif_2_cr_with_upsampling.176x144.bmp) |


Take the images with sequence number `2` to further comparison.

Below are the comparison metrics,
they are computed between the image without sub-sampling
and the other one with sub-sampling and up-sampling in the YCbCr color space:

The image pair on Y plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.00000', '0.00000'],
 ['MSE', '0.00000', '0.00000'],
 ['NRMSE', '0.00000', '0.00000'],
 ['PSNR', 'inf', 'inf'],
 ['SSIM', '1.00000', '1.00000']]
```

The image pair on Cb plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.01417', '0.00000'],
 ['MSE', '0.04257', '0.00000'],
 ['NRMSE', '0.00173', '0.00000'],
 ['PSNR', '61.83934', 'inf'],
 ['SSIM', '0.99984', '1.00000']]
```

The image pair on Cr plane:

```python
[['<Metrics>', '<Score>', '<Goal>'],
 ['MAE', '0.02095', '0.00000'],
 ['MSE', '0.21784', '0.00000'],
 ['NRMSE', '0.00346', '0.00000'],
 ['PSNR', '54.74938', 'inf'],
 ['SSIM', '0.99982', '1.00000']]
```

### Details

The workflow is as follows:

```mermaid
graph LR
    drgb[/Digital RGB Image 0~255/]
    argb([Analog RGB Image 0.~1.])
    tran[Transform RGB to YPbPr with BT.601]
    ayuv([Analog YPbPr Image 0.~1.; -.5~.5])
    dyuv[/Digital YCbCr Image 16~235; 16~240/]
    sub[Sub-sampling 4:2:0]
    ups[Up-sampling from 4:2:0 to 4:4:4]
    pack[Pack YCbCr frames in YUV420p format]

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

Quantize and encode YCbCr `4:2:0` images and recover them.

Taking quantization levels as symbols, here are the Huffman tree and code table used:

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
    437 --> 405
    32:1
    405
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

### Comparison between the images without and with quantization

The quantized versions are visually different from the original RGB images.

The transformed image `0` on different Y, Cb and Cr planes in the grayscale colorspace:

|             | Before quantization | After quantization & de-quantization |
| ----------- | ------------------- | ------------------------------------ |
| On Y plane  | ![](./task_2/foreman_qcif_0_y_with_subsampling.176x144.bmp)  | ![](./task_3/foreman_qcif_0_y_dequantized.176x144.bmp) |
| On Cb plane | ![](./task_2/foreman_qcif_0_cb_with_subsampling.88x72.bmp)   | ![](./task_3/foreman_qcif_0_cb_dequantized.88x72.bmp)  |
| On Cr plane | ![](./task_2/foreman_qcif_0_cr_with_subsampling.88x72.bmp)   | ![](./task_3/foreman_qcif_0_cr_dequantized.88x72.bmp)  |


