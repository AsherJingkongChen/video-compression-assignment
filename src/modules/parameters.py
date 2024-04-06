from numpy import float32, uint8, uint16, uint32, uint64, uint128, uint256
from numpy.typing import ArrayLike, NDArray
from typing import Iterable, Tuple, TypeAlias, Union

uintlike: TypeAlias = Union[uint8, uint16, uint32, uint64, uint128, uint256]


class H273:
    """
    Recommendation ITU-T H.273

    Coding-independent code points for
    video signal type identification

    ## References
    - [ITU](https://www.itu.int/rec/T-REC-H.273-201612-S/en)
    """

    _is_full_range: bool

    def __init__(self) -> None:
        self.set_full_range()

    def set_full_range(self, flag: bool = False) -> "H273":
        """
        Set the video full range flag

        ## Details
        - This flag specifies the scaling and offset values applied
          in association with the other coefficients.
        - When not specified, the value defaults to `False`.

        ## References
        - See Section 8.3 of Rec. ITU-T H.273.
        """

        self._is_full_range = flag
        return self

    @property
    def is_full_range(self) -> bool:
        """
        Get the video full range flag

        ## Details
        - This flag specifies the scaling and offset values applied
          in association with the other coefficients.
        - When not specified, the value defaults to `False`.

        ## References
        - See Section 8.3 of Rec. ITU-T H.273.
        """

        return self._is_full_range

    def quantize_rgb(
        self,
        values: Iterable[Tuple[float32, float32, float32]],
        bit_depth: int = 8,
    ) -> NDArray[uintlike]:
        """
        Quantize the RGB values

        ## Parameters
        - `values`
            - Gamma-corrected RGB values in the range of `0.0` to `1.0`
        - `bit_depth`
            - Representation bit depth of the corresponding luma colour component signal
            - It should be greater than or equal to `8`

        ## Returns
        - Quantized RGB values (`NDArray[uintlike]`)

        ## References
        - See Equation 20 to 22, Section 8 of Rec. ITU-T H.273.
        """

        from numpy import array

        if bit_depth < 8:
            raise ValueError("The bit depth should be greater than or equal to 8")

        bit_depth = int(bit_depth)
        values = array(values, dtype=float32, ndmin=2)

        if self.is_full_range:
            scale = (1 << bit_depth) - 1
            transformed_values = scale * values
            clipped_values = self.clip(transformed_values, bit_depth)
        else:
            padding = 1 << (bit_depth - 8)
            transformed_values = padding * (([219] * 3) * values + ([16] * 3))
            clipped_values = self.clip(transformed_values, bit_depth)

        return clipped_values

    def clip(self, values: ArrayLike, bit_depth: int = 8) -> NDArray[uintlike]:
        """
        Clip the values within the specified bit depth

        ## Parameters
        - `values`: Values to be clipped
        - `bit_depth`: Representation bit depth of the values

        ## Details
        - Formula: `clip(x) = min(max(x, 0), ((1 << bit_depth) - 1))`
        - The values are casted into suitable unsigned integer types

        ## References
        - See Section 5.4 (2), (3), (4) of Rec. ITU-T H.273.
        """

        from numpy import clip

        clipped_values = clip(values, 0, (1 << bit_depth) - 1)
        if bit_depth <= 8:
            return clipped_values.astype(uint8)
        elif bit_depth <= 16:
            return clipped_values.astype(uint16)
        elif bit_depth <= 32:
            return clipped_values.astype(uint32)
        elif bit_depth <= 64:
            return clipped_values.astype(uint64)
        elif bit_depth <= 128:
            return clipped_values.astype(uint128)
        elif bit_depth <= 256:
            return clipped_values.astype(uint256)
