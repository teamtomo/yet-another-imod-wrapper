from os import PathLike
from pathlib import Path
from typing import Dict, Any, List

from .batchruntomo_config.io import read_adoc
from .constants import TARGET_PIXEL_SIZE_FOR_ALIGNMENT, BATCHRUNTOMO_CONFIG_FIDUCIALS
from .utils import (
    find_optimal_power_of_2_binning_factor,
    prepare_imod_directory,
    run_batchruntomo,
    imod_is_installed,
)


def align_using_fiducials(
        tilt_series_file: Path,
        tilt_angles: List[float],
        pixel_size: float,
        fiducial_size: float,
        nominal_rotation_angle: float,
        output_directory: Path,
):
    """Run fiducial based alignment in IMOD on a single tilt-series.

    Parameters
    ----------
    tilt_series_file: file containing tilt-series images.
        File must be compatible with the version of IMOD installed.
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: nominal pixel size in Angstroms per pixel.
    fiducial_size: approximate size of fiducials in nanometers.
    nominal_rotation_angle: initial estimate for the rotation angle of the tilt
        axis. https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    output_directory: tilt-series directory for IMOD.
    """
    if not imod_is_installed():
        raise RuntimeError('No IMOD installation found.')

    prepare_imod_directory(
        tilt_series_file=tilt_series_file,
        tilt_angles=tilt_angles,
        imod_directory=output_directory
    )
    directive = generate_fiducial_alignment_directive(
        tilt_series_file=tilt_series_file,
        pixel_size=pixel_size,
        fiducial_size=fiducial_size,
        rotation_angle=nominal_rotation_angle
    )
    run_batchruntomo(
        tilt_series_file=tilt_series_file,
        imod_directory=output_directory,
        directive=directive
    )


def generate_fiducial_alignment_directive(
        tilt_series_file: PathLike,
        pixel_size: float,
        fiducial_size: float,
        rotation_angle: float
) -> Dict[str, Any]:
    """Generate a fiducial-based alignment directive file for batchruntomo

    Parameters
    ----------
    tilt_series_file : file containing the tilt-series stack
    pixel_size : pixel size in the tilt-series (angstroms per pixel)
    fiducial_size : fiducial size (nanometers)
    rotation_angle : initial estimate for the rotation angle
        https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    """
    alignment_binning_factor = find_optimal_power_of_2_binning_factor(
        src_pixel_size=pixel_size, target_pixel_size=TARGET_PIXEL_SIZE_FOR_ALIGNMENT
    )
    directive = read_adoc(BATCHRUNTOMO_CONFIG_FIDUCIALS)
    directive['setupset.copyarg.stackext'] = Path(tilt_series_file).suffix
    directive['setupset.copyarg.rotation'] = rotation_angle
    directive['setupset.copyarg.pixel'] = pixel_size / 10
    directive['setupset.copyarg.gold'] = fiducial_size
    directive['comparam.prenewst.newstack.BinByFactor'] = alignment_binning_factor
    return directive
