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

    def subsample_444(self, components: NDArray) -> NDArray:
        """
        Subsample chroma components using the scheme `4:4:4`

        ## Parameters
        - `chroma`: Chroma components
            - A NumPy array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - The first (top-left) sample is co-sited with the first Y' or I samples.
        - Each component has the same number of horizontal
          samples as the Y' or I component.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        components = asarray(components)

        if len(components.shape) < 2:
            raise ValueError("The minimum dimension of the components is 2")

        subsampled_components = components[::1, ::1]
        return subsampled_components

    def subsample_422(self, components: NDArray) -> NDArray:
        """
        Subsample chroma components using the scheme `4:2:2`

        ## Parameters
        - `chroma`: Chroma components
            - A NumPy array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - The first (top-left) sample is co-sited with the first Y' or I samples.
        - Horizontally subsampled by a factor of two
          with respect to the Y' or I component.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        components = asarray(components)

        if len(components.shape) < 2:
            raise ValueError("The minimum dimension of the components is 2")

        subsampled_components = components[::1, ::2]
        return subsampled_components

    def subsample_420(self, components: NDArray) -> NDArray:
        """
        Subsample chroma components using the scheme `4:2:0`

        ## Parameters
        - `chroma`: Chroma components
            - A NumPy array with the minimum dimension of 2
            - The shape is represented as `(V, H, ...)`

        ## Returns
        - A NumPy array with the shape of `(V, H, ...)`

        ## Details
        - The first (top-left) sample is co-sited with the first Y' or I samples.
        - Horizontally and vertically subsampled by a factor of two
          with respect to the Y' or I component.

        ## References
        - Table 8 of Rec. ITU-R BT.2100-2
        """

        from numpy import asarray

        components = asarray(components)

        if len(components.shape) < 2:
            raise ValueError("The minimum dimension of the components is 2")

        subsampled_components = components[::2, ::2]
        return subsampled_components
