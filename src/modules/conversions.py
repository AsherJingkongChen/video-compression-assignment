from PIL.Image import Image

# from numpy import typing, uint8


def image_RGB_to_YCbCr(image: Image) -> Image:
    """
    Convert an image from the RGB to YCbCr color space
    using the parameter values of Rec. ITU-R BT.709-6.

    ## Returns

    - A new PIL image in the YCbCr color space
    """

    from numpy import array, uint8
    from .parameters import BT709

    # INT8
    dRGB_list = array(image.convert("RGB").getdata(), dtype=uint8, ndmin=2)
    T, t = BT709.TRANS_AND_OFFSET_RGB_D_TO_A()
    aRGB_list = (T * dRGB_list + t)
    aYCbCr_list = (BT709.TRANS_RGB_TO_YCbCr() @ aRGB_list.T).T
    T, t = BT709.TRANS_AND_OFFSET_YCbCr_A_TO_D()
    dYCbCr_list = (T * aYCbCr_list + t).round().astype(uint8)
    return dYCbCr_list
    # aRGB_list = (dRGB_list / (.max - ).astype(float32)
    # aYCC_list = (BT709.TRANS_RGB_TO_YCbCr() @ aRGB_list.T).T
    # return aYCC_list
    # shape = (image.height, image.width, 3)
    # new_image = Image.fromarray(yuv_list.reshape(shape), mode="YCbCr")
    # return new_image
