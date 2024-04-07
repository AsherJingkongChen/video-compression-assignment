from numpy.typing import NDArray
from typing import BinaryIO, Tuple

from .typing import uintlike


def save_ycbcr_image(
    device: BinaryIO,
    planes: Tuple[NDArray[uintlike], NDArray[uintlike], NDArray[uintlike]],
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


def planar_from_packed(packed_data: NDArray) -> NDArray:
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

def packed_from_planar(planar_data: NDArray) -> NDArray:
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