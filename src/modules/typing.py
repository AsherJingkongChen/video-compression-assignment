from numpy import uint8, uint16, uint32, uint64
from typing import TypeAlias, Union

uintlike: TypeAlias = Union[uint8, uint16, uint32, uint64]
"""
Type alias for unsigned integers with different bit lengths
"""


def get_uint_type(bit_length: int) -> uintlike:
    """
    Get the suitable unsigned integer type based on the bit length
    """
    if bit_length <= 8:
        return uint8
    elif bit_length <= 16:
        return uint16
    elif bit_length <= 32:
        return uint32
    elif bit_length <= 64:
        return uint64
    else:
        raise NotImplementedError("The bit depth is too large")
