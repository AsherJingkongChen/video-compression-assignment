from numpy.typing import ArrayLike, NDArray
from typing import Tuple

def quantize_evenly(
    values: ArrayLike,
    levels: int,
    source_range: Tuple[int, int],
    target_range: Tuple[int, int],
) -> NDArray:
    """
    Quantize values evenly

    ## Parameters
    - `values`: The values to quantize
    - `levels`: The number of levels to use
    - `target_range`: The minimum and maximum of the target
    - `source_range`: The minimum and maximum of the values

    ## Examples

        ```python
        from numpy import array

        values = array([0, 7, 8, 10, 15, 16, 254, 255, 56, 57], dtype=int)
        quantized_values = quantize_evenly(
            values,
            levels=32,
            source_range=(0, 255),
            target_range=(0, 31),
        ).astype(int)

        print(values.tolist())
        print(quantized_values.tolist())

        assert quantized_values.tolist() == [0, 0, 1, 1, 1, 2, 31, 31, 7, 7]
        assert quantized_values.tolist() == (values // (256 // 32)).tolist()
        ```

    ## Returns
    - The quantized values (floored to the nearest integer)

    ## Details
    - Generally, quantization is the process of mapping values
      from a large set to a smaller finite set. This means that
      de-quantization is not a lossless process.
    - This function is for quantization, but it can also
      perform de-quantization by reversing the ranges.
    - Out-of-range values will be scaled as well
    """

    from numpy import array, floor

    values = array(values)
    source_min, source_max = min(source_range), max(source_range)
    target_min, target_max = min(target_range), max(target_range)

    normalized_values = (values - source_min) / (source_max - source_min + 1)
    normalized_leveled_values = floor(normalized_values * levels) / levels
    denormalized_leveled_values = floor(
        normalized_leveled_values * (target_max - target_min + 1) + target_min
    )

    return denormalized_leveled_values
