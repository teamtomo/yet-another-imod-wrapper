import numpy as np

from yet_another_imod_wrapper.utils import (
    find_optimal_power_of_2_binning_factor,
    find_optimal_integer_binning_factor,
    prepare_imod_directory
)


def test_find_optimal_power_of_2_binning_factor():
    result = find_optimal_power_of_2_binning_factor(
        src_pixel_size=2, target_pixel_size=10
    )
    assert result == 4


def test_find_optimal_integer_binning_factor():
    result = find_optimal_integer_binning_factor(
        src_pixel_size=3, target_pixel_size=10,
    )
    assert result == 3


def test_prepare_imod_directory(tmp_path):
    imod_directory = tmp_path / 'imod'
    tilt_series_file = tmp_path / 'my_tilt_series.mrc'
    tilt_series_file.touch()
    tilt_angles = np.arange(-6, 9, 3)

    root_name = tilt_series_file.stem
    prepare_imod_directory(
        tilt_series_file=tilt_series_file,
        tilt_angles=tilt_angles,
        imod_directory=imod_directory
    )

    output_rawtlt_file = imod_directory / f'{root_name}.rawtlt'
    output_tilt_series = imod_directory / tilt_series_file.name
    assert output_rawtlt_file.exists()
    assert output_tilt_series.exists()

    output_tilt_angles = np.loadtxt(output_rawtlt_file)
    assert np.allclose(tilt_angles, output_tilt_angles)
