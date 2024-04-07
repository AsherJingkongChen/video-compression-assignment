from numpy.typing import NDArray


class BT2100:
    """
    Recommendation ITU-R BT.2100-2

    Image parameter values for high dynamic
    range television for use in production and
    international programme exchange

    ## Details
    - Adopts the version on 2018/07

    ## References
    - [Rec. ITU-R BT.2100](https://www.itu.int/rec/R-REC-BT.2100)
    """

    def subsample_444(self, luma: NDArray, chroma: NDArray) -> NDArray:
        """
        Sub-sample chroma components using the scheme `4:4:4`

        ## Parameters
        - `luma`: Luma components
            - An array with the minimum dimension of 2
            - *Unused*
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - The first (top-left) sample is co-sited with the first Y' or I samples.
        - Each chrome component has the same number
          of horizontal samples as the Y' or I component.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        subsampled_chroma = chroma[::1, ::1]
        return subsampled_chroma

    def subsample_422(self, luma: NDArray, chroma: NDArray) -> NDArray:
        """
        Sub-sample chroma components using the scheme `4:2:2`

        ## Parameters
        - `luma`: Luma components
            - An array with the minimum dimension of 2
            - *Unused*
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H / 2, ...)`

        ## Details
        - The first (top-left) sample is co-sited with the first Y' or I samples.
        - Horizontally subsampled by a factor of two
          with respect to the Y' or I component.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        subsampled_chroma = chroma[::1, ::2]
        return subsampled_chroma

    def subsample_420(self, luma: NDArray, chroma: NDArray) -> NDArray:
        """
        Sub-sample chroma components using the scheme `4:2:0`

        ## Parameters
        - `luma`: Luma components
            - An array with the minimum dimension of 2
            - *Unused*
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V / 2, H / 2, ...)`

        ## Details
        - The first (top-left) sample is co-sited with the first Y' or I samples.
        - Horizontally and vertically subsampled by a factor of two
          with respect to the Y' or I component.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        subsampled_chroma = chroma[::2, ::2]
        return subsampled_chroma

    def upsample_444(self, luma: NDArray, chroma: NDArray) -> NDArray:
        """
        Up-sample chroma components which are sub-sampled using the scheme `4:4:4`

        ## Parameters
        - `luma`: Luma components
            - An array with the minimum dimension of 2
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - For sub-sampled input data:
            - The first (top-left) sample is co-sited with the first Y' or I samples.
            - Each chrome component has the same number
              of horizontal samples as the Y' or I component.
        - This method is not officially defined in the standard
        """

        from numpy import asarray, repeat

        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        v, h = luma.shape[:2]
        upscaled_chroma = repeat(repeat(chroma, 1, axis=0), 1, axis=1)
        cropped_chroma = upscaled_chroma[:v, :h, ...]
        return cropped_chroma
    
    def upsample_422(self, luma: NDArray, chroma: NDArray) -> NDArray:
        """
        Up-sample chroma components which are sub-sampled using the scheme `4:2:2`

        ## Parameters
        - `luma`: Luma components
            - An array with the minimum dimension of 2
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2
            - The shape is represented as `(V, H / 2, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - For sub-sampled input data:
            - The first (top-left) sample is co-sited with the first Y' or I samples.
            - Horizontally subsampled by a factor of two
              with respect to the Y' or I component.
        - This method is not officially defined in the standard
        """

        from numpy import asarray, repeat

        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        v, h = luma.shape[:2]
        upscaled_chroma = repeat(repeat(chroma, 1, axis=0), 2, axis=1)
        cropped_chroma = upscaled_chroma[:v, :h, ...]
        return cropped_chroma
    
    def upsample_420(self, luma: NDArray, chroma: NDArray) -> NDArray:
        """
        Up-sample chroma components which are sub-sampled using the scheme `4:2:0`

        ## Parameters
        - `luma`: Luma components
            - An array with the minimum dimension of 2
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2
            - The shape is represented as `(V / 2, H / 2, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - For sub-sampled input data:
            - The first (top-left) sample is co-sited with the first Y' or I samples.
            - Horizontally and vertically subsampled by a factor of two
              with respect to the Y' or I component.
        - This method is not officially defined in the standard
        """

        from numpy import asarray, repeat

        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        v, h = luma.shape[:2]
        upscaled_chroma = repeat(repeat(chroma, 2, axis=0), 2, axis=1)
        cropped_chroma = upscaled_chroma[:v, :h, ...]
        return cropped_chroma
