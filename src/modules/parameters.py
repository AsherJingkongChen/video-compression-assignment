from numpy import float32, typing


class BT709:
    """
    Recommendation ITU-R BT.709-6

    Parameter values for the HDTV standards for
    production and international programme exchange
    """

    def TRANS_RGB_TO_YCbCr(self) -> typing.NDArray[float32]:
        """
        Transformation matrix (`3x3`) from the analog RGB to analog YCbCr color space

        ## Details

        - Formula: `(Y, Cb, Cr) = T @ (R, G, B)`
        - For more information, see Item 3.2 and 3.3 of Rec. ITU-R BT.709-6.
          [(Link)](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf)
        """

        from numpy import array

        return array(
            [
                [+0.2126 / 1.0000, +0.7152 / 1.0000, +0.0722 / 1.0000],
                [-0.2126 / 1.8556, -0.7152 / 1.8556, +0.9278 / 1.8556],
                [+0.7874 / 1.5748, -0.7152 / 1.5748, -0.0722 / 1.5748],
            ],
            dtype=float32,
        )

    def TRANS_YCbCr_TO_RGB(self) -> typing.NDArray[float32]:
        """
        Transformation matrix (`3x3`) from the analog YCbCr to analog RGB color space

        ## Details

        - Formula: `(R, G, B) = T @ (Y, Cb, Cr)`
        - This matrix is the inverse of `BT709.TRANS_RGB_TO_YCbCr()`.
        - For more information, see Item 3.2 and 3.3 of Rec. ITU-R BT.709-6.
          [(Link)](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf)
        """

        from numpy import linalg

        return linalg.inv(self.TRANS_RGB_TO_YCbCr())

    def TRANS_AND_OFFSET_RGB_A_TO_D(
        self,
    ) -> tuple[typing.NDArray[float32], typing.NDArray[float32]]:
        """
        Arguments for transformation from the analog RGB to digital RGB color space

        ## Returns

        1. Transformation vector `T` (`3x1`)
        2. Offset vector `t` (`3x1`)

        ## Details

        - Formula: `(dR, dG, dB) = T * (aR, aG, aB) + t`
        - Ranges: `aR, aG, aB ∈ [0.0, 1.0]` and `dR, dG, dB ∈ [16, 235]`
        - For more information, see Item 3.4 and 4.6 of Rec. ITU-R BT.709-6.
          [(Link)](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf)
        """
        from numpy import array

        transform = array([219, 219, 219], dtype=float32)
        offset = array([16, 16, 16], dtype=float32)
        return (transform, offset)

    def TRANS_AND_OFFSET_RGB_D_TO_A(
        self,
    ) -> tuple[typing.NDArray[float32], typing.NDArray[float32]]:
        """
        Arguments for transformation from the digital RGB to analog RGB color space

        ## Returns

        1. Transformation vector `T` (`3x1`)
        2. Offset vector `t` (`3x1`)

        ## Details

        - Formula: `(aR, aG, aB) = T * (dR, dG, dB) - t`
        - Ranges: `aR, aG, aB ∈ [0.0, 1.0]` and `dR, dG, dB ∈ [16, 235]`
        - For more information, see Item 3.4 and 4.6 of Rec. ITU-R BT.709-6.
          [(Link)](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf)
        """

        transform, offset = self.TRANS_AND_OFFSET_RGB_A_TO_D()
        transform = 1 / transform
        offset = -offset * transform
        return (transform, offset)

    def TRANS_AND_OFFSET_YCbCr_A_TO_D(
        self,
    ) -> tuple[typing.NDArray[float32], typing.NDArray[float32]]:
        """
        Arguments for transformation from the analog YCbCr to digital YCbCr color space

        ## Returns

        1. Transformation vector `T` (`3x1`)
        2. Offset vector `t` (`3x1`)

        ## Details

        - Formula: `(dY, dCb, dCr) = T * (aY, aCb, aCr) + t`
        - Ranges: `aY ∈ [0.0, 1.0], aCb, aCr ∈ [-0.5, +0.5]` and
                  `dY ∈ [16, 235], dCb, dCr ∈ [16, 240]`
        - For more information, see Item 3.4 and 4.6 of Rec. ITU-R BT.709-6.
          [(Link)](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf)
        """
        from numpy import array

        transform = array([219, 224, 224], dtype=float32)
        offset = array([16, 128, 128], dtype=float32)
        return (transform, offset)

    def TRANS_AND_OFFSET_YCbCr_D_TO_A(
        self,
    ) -> tuple[typing.NDArray[float32], typing.NDArray[float32]]:
        """
        Arguments for transformation from the digital YCbCr to analog YCbCr color space

        ## Returns

        1. Transformation vector `T` (`3x1`)
        2. Offset vector `t` (`3x1`)

        ## Details

        - Formula: `(dY, dCb, dCr) = T * (aY, aCb, aCr) + t`
        - Ranges: `aY ∈ [0.0, 1.0], aCb, aCr ∈ [-0.5, +0.5]` and
                  `dY ∈ [16, 235], dCb, dCr ∈ [16, 240]`
        - For more information, see Item 3.4 and 4.6 of Rec. ITU-R BT.709-6.
          [(Link)](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.709-6-201506-I!!PDF-E.pdf)
        """

        transform, offset = self.TRANS_AND_OFFSET_YCbCr_A_TO_D()
        transform = 1 / transform
        offset = -offset * transform
        return (transform, offset)
