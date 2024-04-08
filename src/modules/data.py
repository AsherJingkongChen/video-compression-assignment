from numpy.typing import ArrayLike, NDArray
from typing import BinaryIO, Iterable, Tuple, Union

from ..modules.typing import get_uint_type


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
    - `size`: The width and height of the image
    - `subsampling_scheme`: The sub-sampling scheme used for the image file
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
    from numpy import frombuffer, ceil, uint8

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

    # Calculate the number of bytes per pixel
    byte_per_pixel_y, byte_per_pixel_cb, byte_per_pixel_cr = (
        int(ceil(bit_per_pixel_y / 8)),
        int(ceil(bit_per_pixel_cb / 8)),
        int(ceil(bit_per_pixel_cr / 8)),
    )

    # Calculate the number of pixels in each plane
    h_luma, v_luma = size
    j, a, b = subsampling_scheme
    dh, dv = j // a, j // (a + b)
    h_chroma, v_chroma = int(ceil(h_luma / dh)), int(ceil(v_luma / dv))
    pixels_y, pixels_cb, pixels_cr = (
        h_luma * v_luma,
        h_chroma * v_chroma,
        h_chroma * v_chroma,
    )

    # Calculate the number of bytes in each plane
    bytes_y, bytes_cb, bytes_cr = (
        byte_per_pixel_y * pixels_y,
        byte_per_pixel_cb * pixels_cb,
        byte_per_pixel_cr * pixels_cr,
    )

    plane_y = frombuffer(
        device.read(bytes_y), dtype=get_uint_type(bit_per_pixel_y)
    ).reshape(v_luma, h_luma)
    plane_cb = frombuffer(
        device.read(bytes_cb), dtype=get_uint_type(bit_per_pixel_cb)
    ).reshape(v_chroma, h_chroma)
    plane_cr = frombuffer(
        device.read(bytes_cr), dtype=get_uint_type(bit_per_pixel_cr)
    ).reshape(v_chroma, h_chroma)
    return (plane_y, plane_cb, plane_cr)


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
