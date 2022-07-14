import os
import shutil
from pathlib import Path

from packaging import version

from yet_another_imod_wrapper.constants import MINIMUM_IMOD_VERSION


def check_imod_installation() -> None:
    """Check that IMOD is installed and satisfies the minimum version requirements."""
    if not _imod_is_installed():
        raise RuntimeError('No IMOD installation found.')
    imod_version = _get_imod_version()
    if imod_version < version.parse(MINIMUM_IMOD_VERSION):
        raise RuntimeError(f'Ensure IMOD version {MINIMUM_IMOD_VERSION} or higher is installed. '
                           f'Your version is {imod_version}')


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
