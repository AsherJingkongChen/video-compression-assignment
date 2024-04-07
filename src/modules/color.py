from numpy import float32, uint8, uint16, uint32, uint64
from numpy.typing import ArrayLike, NDArray
from typing import Iterable, Tuple, TypeAlias, Union

uintlike: TypeAlias = Union[uint8, uint16, uint32, uint64]


class H273:
    """
    Recommendation ITU-T H.273

    Coding-independent code points for
    video signal type identification

    ## References
    - [ITU](https://www.itu.int/rec/T-REC-H.273-201612-S/en)
    """

    _is_full_range: bool
    _is_rgb_gamma_corrected: bool

    def __init__(
        self,
        *,
        full_range: bool = False,
        rgb_gamma_corrected: bool = True,
    ) -> None:
        self.set_full_range(full_range)
        self.set_rgb_gamma_corrected(rgb_gamma_corrected)

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

    def set_rgb_gamma_corrected(self, flag: bool = True) -> "H273":
        """
        Set the RGB gamma-corrected flag

        ## Details
        - This flag specifies whether the input RGB values
          are assumed to be gamma-corrected.
        - When not specified, the value defaults to `True`.
        - *Case for `False` is not implemented yet*

        ## References
        - See Section 8.2 of Rec. ITU-T H.273.
        """

        if not flag:
            raise NotImplementedError("Case for `False` is not implemented yet")

        self._is_rgb_gamma_corrected = flag
        return self

    @property
    def is_rgb_gamma_corrected(self) -> bool:
        """
        Get the RGB gamma-corrected flag

        ## Details
        - This flag specifies whether the input RGB values
          are assumed to be gamma-corrected.
        - When not specified, the value defaults to `True`.
        - *Case for `False` is not implemented yet*

        ## References
        - See Section 8.2 of Rec. ITU-T H.273.
        """

        return self._is_rgb_gamma_corrected

    def quantize_rgb(
        self,
        values: Iterable[Tuple[float32, float32, float32]],
        bit_depth: int = 8,
    ) -> NDArray[uintlike]:
        """
        Quantize the RGB values (from analog to digital)

        ## Parameters
        - `values`
            - Gamma-corrected RGB values in the range of `0.0` to `1.0` *[Section 8.3]*
        - `bit_depth`
            - Representation bit depth of the corresponding luma colour component signal
            - It should be greater than or equal to `8`
            - The default value is `8`

        ## Returns
        - Quantized RGB values (`NDArray[uintlike]`)

        ## References
        - See Equation 20 to 22, 26 to 28, Section 8 of Rec. ITU-T H.273.
        """

        from numpy import array

        if not self.is_rgb_gamma_corrected:
            raise ValueError("The input RGB values are assumed to be gamma-corrected")
        if bit_depth < 8:
            raise ValueError("The bit depth should be greater than or equal to 8")

        bit_depth = int(bit_depth)
        values = array(values, dtype=float32, ndmin=2).reshape(-1, 3)

        if self.is_full_range:
            scale = (1 << bit_depth) - 1
            transformed_values = scale * values
            clipped_values = self.clip(transformed_values, bit_depth)
        else:
            padding = 1 << (bit_depth - 8)
            transformed_values = padding * (219 * values + 16)
            clipped_values = self.clip(transformed_values, bit_depth)

        return clipped_values

    def quantize_ypbpr(
        self,
        values: Iterable[Tuple[float32, float32, float32]],
        bit_depth_y: int = 8,
        bit_depth_cb: int = 8,
        bit_depth_cr: int = 8,
    ) -> NDArray[uintlike]:
        """
        Quantize the YPbPr values into YCbcCr values (from analog to digital)

        ## Parameters
        - `values`
            - YPbPr values
            - The Y values are in the range of `0.0` to `1.0`
            - The Pb and Pr values are in the range of `-0.5` to `0.5`
        - `bit_depth_y`
            - Representation bit depth of the corresponding luma colour component signal
            - It should be greater than or equal to `8`
            - The default value is `8`
        - `bit_depth_cb`
            - Representation bit depth of the blue-difference chroma colour component signal
            - It should be greater than or equal to `8`
            - The default value is `8`
        - `bit_depth_cr`
            - Representation bit depth of the red-difference chroma colour component signal
            - It should be greater than or equal to `8`
            - The default value is `8`

        ## Returns
        - Quantized YCbcCr values (`NDArray[uintlike]`)
            - The data types are determined based on the largest bit depths (Y, Cb, Cr)

        ## Details
        - The bit depths for chroma components might be distinct. *[Equation 3, Section 5.4]*

        ## References
        - See Equation 23 to 25, 29 to 31, Section 8 of Rec. ITU-T H.273.
        """

        from numpy import array, stack

        if bit_depth_y < 8:
            raise ValueError("The bit depth y should be greater than or equal to 8")
        if bit_depth_cb < 8:
            raise ValueError("The bit depth cb should be greater than or equal to 8")
        if bit_depth_cr < 8:
            raise ValueError("The bit depth cr should be greater than or equal to 8")

        bit_depth_y, bit_depth_cb, bit_depth_cr = map(
            int, (bit_depth_y, bit_depth_cb, bit_depth_cr)
        )
        values = array(values, dtype=float32, ndmin=2).reshape(-1, 3)

        if self.is_full_range:
            scale = (
                1 << array([bit_depth_y, bit_depth_cb, bit_depth_cr], dtype=uint32)
            ) - 1
            padding = 1 << (array([1, bit_depth_cb, bit_depth_cr], dtype=uint32) - 1)
            padding[0] = 0
            transformed_values = (scale * values + padding).round()
        else:
            padding = 1 << (
                array([bit_depth_y, bit_depth_cb, bit_depth_cr], dtype=uint32) - 8
            )
            transformed_values = (
                padding * ([219, 224, 224] * values + [16, 128, 128])
            ).round()

        unclipped_values = transformed_values.T
        clipped_values = stack(
            [
                self.clip(unclipped_values[0], bit_depth_y),
                self.clip(unclipped_values[1], bit_depth_cb),
                self.clip(unclipped_values[2], bit_depth_cr),
            ],
            axis=1,
        )
        return clipped_values

    def rgb_from_ypbpr(
        self,
        values: Iterable[Tuple[float32, float32, float32]],
        kr: float32,
        kb: float32,
    ) -> NDArray[float32]:
        """
        Compute the RGB values from the YPbPr values (from analog to analog)

        ## Parameters
        - `values`
            - YPbPr values
            - The Y values are in the range of `0.0` to `1.0` *[Note 3]*
            - The Pb and Pr values are in the range of `-0.5` to `0.5` *[Note 3]*
        - `kr`
            - Constant `Kr` computed from color primaries *[Table 4]*
        - `kb`
            - Constant `Kb` computed from color primaries *[Table 4]*

        ## Returns
        - RGB values (`NDArray[float32]`)
            - RGB values are in the range of `0.0` to `1.0`

        ## Details
        - The implementation differs on whether the RGB values are gamma-corrected or not
            - *Case for `False` is not implemented yet*
        - It is implemented as the inverse operation of `ypbpr_from_rgb`

        ## References
        - See Equation 38 to 40, 59 to 68 Section 8 of Rec. ITU-T H.273.
        """

        from numpy import array, linalg

        values = array(values, dtype=float32, ndmin=2).reshape(-1, 3)

        if self.is_rgb_gamma_corrected:
            transform_matrix = linalg.inv(self.get_ypbpr_transformation_matrix(kr, kb))
            transposed_values = values.T
            transformed_values = (transform_matrix * transposed_values).T
        else:
            raise NotImplementedError("Case for `False` is not implemented yet")

        return transformed_values

    def ypbpr_from_rgb(
        self,
        values: Iterable[Tuple[float32, float32, float32]],
        kr: float32,
        kb: float32,
    ) -> NDArray[float32]:
        """
        Compute the YPbPr values from the RGB values (from analog to analog)

        ## Parameters
        - `values`
            - RGB values in the range of `0.0` to `1.0`
        - `kr`
            - Constant `Kr` computed from color primaries *[Table 4]*
        - `kb`
            - Constant `Kb` computed from color primaries *[Table 4]*

        ## Returns
        - YPbPr values (`NDArray[float32]`)
            - The Y values are in the range of `0.0` to `1.0` *[Note 3]*
            - The Pb and Pr values are in the range of `-0.5` to `0.5` *[Note 3]*

        ## Details
        - The implementation differs on whether the RGB values are gamma-corrected or not
            - *Case for `False` is not implemented yet*

        ## References
        - See Equation 38 to 40, 59 to 68 Section 8 of Rec. ITU-T H.273.
        """

        from numpy import array

        values = array(values, dtype=float32, ndmin=2).reshape(-1, 3)

        if self.is_rgb_gamma_corrected:
            transform_matrix = self.get_ypbpr_transformation_matrix(kr, kb)
            transposed_values = values.T
            transformed_values = (transform_matrix * transposed_values).T
        else:
            raise NotImplementedError("Case for `False` is not implemented yet")

        return transformed_values

    def get_ypbpr_transformation_matrix(
        self,
        kr: float32,
        kb: float32,
    ) -> NDArray[float32]:
        """
        Compute the transformation matrix from the RGB color space to the YPbPr one

        ## Parameters
        - `kr`
            - Constant `Kr` computed from color primaries *[Table 4]*
        - `kb`
            - Constant `Kb` computed from color primaries *[Table 4]*

        ## Returns
        - Transformation matrix (`NDArray[float32]`)
            - Shape: `(3, 3)`

        ## Details
        - Formula:

            ```plaintext
            Kg = 1 - Kr - Kb
            Y  = (    Kr * R + Kg * G +     Kb * B)
            Pb = (    Kr * R + Kg * G + (Kb-1) * B) * (-0.5 / (1 - Kb))
            Pr = ((Kr-1) * R + Kg * G + (Kb-1) * B) * (-0.5 / (1 - Kr))
            ```

        ## References
        - See Equation 38 to 40, Section 8 of Rec. ITU-T H.273.
        """

        from numpy import array

        kg = 1 - kr - kb
        transformation_matrix = array([[kr, kg, kb]] * 3, dtype=float32)
        transformation_matrix[1][2] -= 1
        transformation_matrix[2][0] -= 1
        transformation_matrix[1] *= -0.5 / (1 - kb)
        transformation_matrix[2] *= -0.5 / (1 - kr)
        return transformation_matrix

    def clip(self, values: ArrayLike, bit_depth: int = 8) -> NDArray[uintlike]:
        """
        Clip the values within the specified bit depth

        ## Parameters
        - `values`: Values to be clipped
        - `bit_depth`:
            - Representation bit depth of the values
            - It should be greater than or equal to `0`

        ## Returns
        - Clipped values (`NDArray[uintlike]`)

        ## Details
        - Formula: `clip(x) = min(max(x, 0), ((1 << bit_depth) - 1))`
        - The values are casted into suitable unsigned integer types

        ## References
        - See Equation 2 to 4, Section 5.4 of Rec. ITU-T H.273.
        """

        from numpy import clip

        if bit_depth < 0:
            raise ValueError("The bit depth should be greater than or equal to 0")

        clipped_values = clip(values, 0, (1 << bit_depth) - 1)

        if bit_depth <= 8:
            return clipped_values.astype(uint8)
        elif bit_depth <= 16:
            return clipped_values.astype(uint16)
        elif bit_depth <= 32:
            return clipped_values.astype(uint32)
        elif bit_depth <= 64:
            return clipped_values.astype(uint64)
        else:
            raise NotImplementedError("The bit depth is too large")
