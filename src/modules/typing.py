from numpy import uint8, uint16, uint32, uint64
from typing import TypeAlias, Union

uintlike: TypeAlias = Union[uint8, uint16, uint32, uint64]
"""Type alias for unsigned integers with different bit lengths."""
