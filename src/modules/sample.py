from numpy.typing import ArrayLike, NDArray
from typing import Tuple


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

    def subsample(
        self,
        scheme: Tuple[int, int, int],
        luma: ArrayLike,
        chroma: ArrayLike,
    ) -> NDArray:
        """
        Sub-sample the chroma components using the given scheme

        ## Parameters
        - `scheme`: Colour sub-sampling scheme to use
        - `luma`: Luma components
            - An array with the minimum dimension of 2
            - *Unused*
        - `chroma`: Chroma components
            - An array with the minimum dimension of 2

        ## Returns
        - A NumPy array transformed from the chroma components

        ## Details
        - To find valid values of `scheme`, search for the methods
          beginning with `SUBSAMPLING_SCHEME_` in this module.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        j, a, b = map(int, scheme)
        luma = asarray(luma)
        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        dv, dh = j // (a + b), j // a
        subsampled_chroma = chroma[::dv, ::dh]
        return subsampled_chroma

    def upsample(
        self,
        scheme: Tuple[int, int, int],
        luma: ArrayLike,
        chroma: ArrayLike,
    ) -> NDArray:
        """
        Up-sample the chroma components using the given scheme

        ## Parameters
        - `scheme`: Colour sub-sampling scheme used
        - `luma`: Luma components which are referenced
            - An array with the minimum dimension of 2
        - `chroma`: Chroma components which are sub-sampled
            - An array with the minimum dimension of 2

        ## Returns
        - A NumPy array transformed from the chroma components

        ## Details
        - To find valid values of `scheme`, search for the methods
          beginning with `SUBSAMPLING_SCHEME_` in this module.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray, repeat

        j, a, b = map(int, scheme)
        luma = asarray(luma)
        chroma = asarray(chroma)

        if luma.ndim < 2 or chroma.ndim < 2:
            raise ValueError("The minimum dimension of the components is 2")

        v, h = luma.shape[:2]
        dv, dh = j // (a + b), j // a
        upscaled_chroma = repeat(repeat(chroma, dv, axis=0), dh, axis=1)
        cropped_chroma = upscaled_chroma[:v, :h, ...]
        return cropped_chroma


def SUBSAMPLING_SCHEME_420() -> Tuple[int, int, int]:
    """
    Colour sub-sampling scheme `4:2:0`

    ## Details
    - The first (top-left) sample is co-sited
        with the first Y' or I samples
    - Horizontally and vertically subsampled by a factor of two
        with respect to the Y' or I component
    - The shape of sub-sampled components will be
        `(V / 2, H / 2, ...)` while the original one is `(V, H, ...)`

    ## References
    - Table 8 of Rec. ITU-R BT.2100-2
    """

    return (4, 2, 0)


def SUBSAMPLING_SCHEME_422() -> Tuple[int, int, int]:
    """
    Colour sub-sampling scheme `4:2:2`

    ## Details
    - The first (top-left) sample is co-sited
        with the first Y' or I samples
    - Horizontally subsampled by a factor of two
        with respect to the Y' or I component
    - The shape of sub-sampled components will be
        `(V, H / 2, ...)` while the original one is `(V, H, ...)`

    ## References
    - Table 8 of Rec. ITU-R BT.2100-2
    """

    return (4, 2, 2)


def SUBSAMPLING_SCHEME_444() -> Tuple[int, int, int]:
    """
    Colour sub-sampling scheme `4:4:4`

    ## Details
    - The first (top-left) sample is co-sited
        with the first Y' or I samples
    - Each chrome component has the same number
        of horizontal samples as the Y' or I component
    - The shape of sub-sampled components will be
        `(V, H, ...)` while the original one is `(V, H, ...)`

    ## References
    - Table 8 of Rec. ITU-R BT.2100-2
    """

    return (4, 4, 4)
