import numpy as np


def find_optimal_integer_binning_factor(
        src_pixel_size: float, target_pixel_size: float
) -> int:
    binning_factors = np.arange(1, 30)
    return _find_optimal_binning_factor(binning_factors, src_pixel_size, target_pixel_size)


def find_optimal_power_of_2_binning_factor(
        src_pixel_size: float, target_pixel_size: float
) -> int:
    binning_factors = 2 ** np.arange(6)
    return _find_optimal_binning_factor(binning_factors, src_pixel_size, target_pixel_size)


def _find_optimal_binning_factor(
        binning_factors: np.ndarray,
        src_pixel_size: float,
        target_pixel_size: float
) -> int:
    binned_pixel_sizes = binning_factors * src_pixel_size
    pixel_size_deltas = np.abs(binned_pixel_sizes - target_pixel_size)
    return binning_factors[np.argmin(pixel_size_deltas)]
