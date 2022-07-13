import os
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Sequence, List

import mrcfile
from packaging import version

import numpy as np

from .batchruntomo_config.io import write_adoc
from .constants import MINIMUM_IMOD_VERSION
from .etomo_directory import EtomoDirectory


def check_imod_installation() -> None:
    """Check that IMOD is installed and satisfies the minimum version requirements."""
    if not _imod_is_installed():
        raise RuntimeError('No IMOD installation found.')
    imod_version = _get_imod_version()
    if imod_version < version.parse(MINIMUM_IMOD_VERSION):
        raise RuntimeError(f'Ensure IMOD version {MINIMUM_IMOD_VERSION} or higher is installed. '
                           f'Your version is {imod_version}')


def prepare_etomo_directory(
        directory: Path,
        tilt_series: np.ndarray,
        tilt_angles: Sequence[float],
        basename: str,
) -> EtomoDirectory:
    """Prepare a directory for IMOD tilt-series alignment."""
    directory.mkdir(exist_ok=True, parents=True)
    directory = EtomoDirectory(basename=basename, directory=directory)
    mrcfile.write(str(directory.tilt_series_file), tilt_series.astype(np.float32))
    np.savetxt(directory.rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')
    return directory


def _get_batchruntomo_command(
        directory: Path, basename: str, directive_file: Path
) -> List[str]:
    """Get batchruntomo command."""
    command = [
        'batchruntomo',
        '-DirectiveFile', f'{directive_file}',
        '-CurrentLocation', f'{directory}',
        '-RootName', basename,
        '-EndingStep', '6'
    ]
    return command


def run_batchruntomo(
        directory: Path, basename: str, directive: Dict[str, str]
) -> None:
    """Run batchruntomo on a single tilt-series with a specified directive."""
    with tempfile.TemporaryDirectory() as temporary_directory:
        directive_file = Path(temporary_directory) / 'directive.adoc'
        write_adoc(directive, directive_file)
        batchruntomo_command = _get_batchruntomo_command(
            directory=directory,
            basename=basename,
            directive_file=directive_file
        )
        subprocess.run(batchruntomo_command)


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


def force_symlink(src: Path, link_name: Path) -> None:
    """Force creation of a symbolic link, removing any existing file."""
    if link_name.exists():
        os.remove(link_name)
    os.symlink(src, link_name)


def _imod_is_installed() -> bool:
    """Check if IMOD is installed and on the PATH."""
    return shutil.which('imod') is not None


def _get_imod_directory() -> Path:
    """Get path to IMOD installation."""
    imod_dir = os.environ.get('IMOD_DIR')
    if imod_dir is None:
        raise ValueError('IMOD_DIR is not set, please check your IMOD installation.')
    return Path(imod_dir)


def _get_imod_version() -> version.Version:
    """Get IMOD version."""
    imod_dir = _get_imod_directory()
    with open(imod_dir / 'VERSION') as f:
        return version.parse(f.readline().strip())
