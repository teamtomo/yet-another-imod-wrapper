import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict

import numpy as np

from yet_another_imod_wrapper.batchruntomo_config.io import write_adoc


def imod_is_installed() -> bool:
    """Check if batchruntomo is on the PATH."""
    return shutil.which('batchruntomo') is not None


def prepare_imod_directory(
        tilt_series_file: Path, tilt_angles: List[float], imod_directory: Path
):
    root_name = tilt_series_file.stem
    imod_directory.mkdir(exist_ok=True, parents=True)

    tilt_series_file_for_imod = imod_directory / tilt_series_file.name
    force_symlink(tilt_series_file.absolute(), tilt_series_file_for_imod)

    rawtlt_file = imod_directory / f'{root_name}.rawtlt'
    np.savetxt(rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')


def run_batchruntomo(
        tilt_series_file: Path, imod_directory: Path, directive: Dict[str, str]
):
    root_name = tilt_series_file.stem
    with tempfile.TemporaryDirectory() as temporary_directory:
        directive_file = Path(temporary_directory) / 'directive.adoc'
        write_adoc(directive, directive_file)
        batchruntomo_command = [
            'batchruntomo',
            '-DirectiveFile', f'{directive_file}',
            '-RootName', f'{root_name}',
            '-CurrentLocation', f'{imod_directory}',
            '-EndingStep', '6'
        ]
        subprocess.run(batchruntomo_command)


def _find_optimal_binning_factor(
        binning_factors: np.ndarray,
        src_pixel_size: float,
        target_pixel_size: float
) -> int:
    binned_pixel_sizes = binning_factors * src_pixel_size
    pixel_size_deltas = np.abs(binned_pixel_sizes - target_pixel_size)
    return binning_factors[np.argmin(pixel_size_deltas)]


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


def force_symlink(src: Path, link_name: Path):
    """Force creation of a symbolic link, removing any existing file."""
    if link_name.exists():
        os.remove(link_name)
    os.symlink(src, link_name)
