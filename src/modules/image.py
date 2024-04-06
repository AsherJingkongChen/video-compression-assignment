from dataclasses import dataclass
from PIL.Image import Image

from .parameters import BT709


@dataclass
class YUVImage:
    """
    Digitally represents a YUV image in the specific YCbCr color space
    """

    from numpy import typing, uint8

    width: int
    "The width of the image"

    height: int
    "The height of the image"

    y_plane: typing.NDArray[uint8]
    "A NumPy array containing the image data on Y plane with shape `(height, width)`"

    u_plane: typing.NDArray[uint8]
    "A NumPy array containing the image data on Y plane with shape not greater than `(height, width)`"

    v_plane: typing.NDArray[uint8]
    "A NumPy array containing the image data on Y plane with shape not greater than `(height, width)`"

    def __post_init__(self):
        assert self.y_plane.shape == self.shape, (self.y_plane.shape, self.shape)
        assert self.u_plane.shape <= self.shape, (self.u_plane.shape, self.shape)
        assert self.v_plane.shape <= self.shape, (self.v_plane.shape, self.shape)

    @staticmethod
    def from_pil_image(image: Image, recommendation=BT709()):
        """
        Initialize a new YUV image from a PIL image using the given recommendation
        """
        from numpy import array, uint8

        image = image.convert("RGB")
        dRGB_list = array(image.getdata(), dtype=uint8, ndmin=2)
        T, t = recommendation.TRANS_AND_OFFSET_RGB_D_TO_A()
        aRGB_list = T * dRGB_list + t
        aYCbCr_list = (recommendation.TRANS_RGB_TO_YCbCr() @ aRGB_list.T).T
        T, t = recommendation.TRANS_AND_OFFSET_YCbCr_A_TO_D()
        dYCbCr_list = (T * aYCbCr_list + t).round().astype(uint8)
        dYCbCr_planes = dYCbCr_list.T.reshape((3, image.height, image.width))
        return YUVImage(*image.size, *dYCbCr_planes)

    @property
    def shape(self) -> tuple[int, int]:
        "The shape of the image data in the form `(height, width)`"
        return (self.height, self.width)

    @property
    def size(self) -> tuple[int, int]:
        "The size of the image in the form `(width, height)`"
        return (self.width, self.height)
