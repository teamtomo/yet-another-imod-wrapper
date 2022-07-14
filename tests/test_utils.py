import numpy as np
import mrcfile

from yet_another_imod_wrapper import utils


def test_find_optimal_power_of_2_binning_factor():
    result = utils.binning.find_optimal_power_of_2_binning_factor(
        src_pixel_size=2, target_pixel_size=10
    )
    assert result == 4


def test_find_optimal_integer_binning_factor():
    result = utils.binning.find_optimal_integer_binning_factor(
        src_pixel_size=3, target_pixel_size=10,
    )
    assert result == 3


def test_prepare_etomo_directory(tmp_path):
    directory = tmp_path / 'imod'
    basename = 'TS'
    tilt_series = np.arange(41 * 100).reshape((41, 10, 10))
    tilt_angles = np.arange(-60, 63, 3)
    etomo_directory = utils.etomo.prepare_etomo_directory(
        tilt_series=tilt_series,
        tilt_angles=tilt_angles,
        basename=basename,
        directory=directory
    )

    assert etomo_directory.tilt_series_file.exists()
    output_tilt_series = mrcfile.read(etomo_directory.tilt_series_file)
    assert np.allclose(output_tilt_series, tilt_series)

    assert etomo_directory.rawtlt_file.exists()
    output_tilt_angles = np.loadtxt(etomo_directory.rawtlt_file)
    assert np.allclose(tilt_angles, output_tilt_angles)


def test_get_batchruntomo_command(tmp_path):
    basename = 'base'
    directive_file = tmp_path / 'directive'
    result = utils.etomo._get_batchruntomo_command(
        directory=tmp_path,
        basename=basename,
        directive_file=directive_file
    )
    assert result == [
        'batchruntomo',
        '-DirectiveFile', f'{directive_file}',
        '-CurrentLocation', f'{tmp_path}',
        '-RootName', basename,
        '-EndingStep', '6'
    ]
