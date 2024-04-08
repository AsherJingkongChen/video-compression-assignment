from numpy.typing import ArrayLike, NDArray
from typing import BinaryIO, Iterable, Tuple, Union


def save_ycbcr_image(
    device: BinaryIO,
    planes: Tuple[ArrayLike, ArrayLike, ArrayLike],
) -> None:
    """
    Save a YCbCr image to a writable device.

    ## Parameters
    - `device`: A writable binary device to save the image to
    - `planes`: The Y, Cb, and Cr planes of the image
        - Each plane is an array of unsigned integers
          with the minimum dimension of 2

    ## Returns
    - `None`

    ## Details
    - The arrays in `planes` will be represented as byte sequences and
      be written to the device in the order Y, Cb, Cr.
    """

    from io import BufferedIOBase, RawIOBase
    from numpy import asarray

    if not device.writable():
        raise ValueError("The device is not writable")
    if not isinstance(device, (BufferedIOBase, RawIOBase)):
        raise ValueError("The device must be in binary mode")
    if len(planes) != 3:
        raise ValueError("The number of planes must be 3")

    for plane in planes:
        plane = asarray(plane)

        if plane.ndim < 2:
            raise ValueError("The minimum dimension of the plane is 2")

        device.write(plane.tobytes())


def load_ycbcr_image(
    device: BinaryIO,
    size: Tuple[int, int],
    subsampling_scheme: Tuple[int, int, int],
    bit_per_pixel_y: int = 8,
    bit_per_pixel_cb: int = 8,
    bit_per_pixel_cr: int = 8,
) -> Tuple[NDArray, NDArray, NDArray]:
    """
    Load a YCbCr image from a readable device.

    ## Parameters
    - `device`: A readable binary device to load the image from
    - `size`: The dimensions of the image in the order width, height
    - `subsampling_scheme`: The subsampling scheme used for the image file
        - A tuple of three integers representing the scheme
        - Search for the methods beginning
          with `SUBSAMPLING_SCHEME_` in the `sample` module

    ## Returns
    - A tuple of the Y, Cb, and Cr planes of the image
        - Each plane is a NumPy array of unsigned integers

    ## Details
    - The image file is assumed to be in the planar format,
      or saved using `save_ycbcr_image` function
    """

    from io import BufferedIOBase, RawIOBase
    from numpy import asarray

    bit_per_pixel_y, bit_per_pixel_cb, bit_per_pixel_cr = map(
        int, (bit_per_pixel_y, bit_per_pixel_cb, bit_per_pixel_cr)
    )

    if not device.readable():
        raise ValueError("The device is not readable")
    if not isinstance(device, (BufferedIOBase, RawIOBase)):
        raise ValueError("The device must be in binary mode")
    if len(size) != 2:
        raise ValueError("The number of sizes must be 2")
    if len(subsampling_scheme) != 3:
        raise ValueError("The number of subsampling schemes must be 3")
    if bit_per_pixel_y < 8 or bit_per_pixel_cb < 8 or bit_per_pixel_cr < 8:
        raise ValueError("The bits per pixel must be at least 8")


def planar_from_packed(packed_data: ArrayLike) -> Union[NDArray, Iterable[NDArray]]:
    """
    Represent packed data in the planar format.

    ## Parameters
    - `packed_data`: An array in the shape of `(..., N)`

    ## Returns
    - An array in the shape of `(N, ...)`
    """

    from numpy import asarray, moveaxis

    packed_data = asarray(packed_data)
    planar_data = moveaxis(packed_data, -1, 0)

    return planar_data


def packed_from_planar(planar_data: Union[NDArray, Iterable[NDArray]]) -> NDArray:
    """
    Represent planar data in the packed format.

    ## Parameters
    - `planar_data`: An array in the shape of `(N, ...)`

    ## Returns
    - An array in the shape of `(..., N)`
    """

    from numpy import asarray, moveaxis

    planar_data = asarray(planar_data)
    packed_data = moveaxis(planar_data, 0, -1)

    return packed_data
