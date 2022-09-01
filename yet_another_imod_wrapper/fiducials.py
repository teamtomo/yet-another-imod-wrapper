from os import PathLike
from pathlib import Path
from typing import Dict, Any, List

import numpy as np

from .utils.io import read_adoc
from .constants import TARGET_PIXEL_SIZE_FOR_ALIGNMENT, BATCHRUNTOMO_CONFIG_FIDUCIALS
from .utils.binning import find_optimal_power_of_2_binning_factor
from .utils.etomo import prepare_etomo_directory, run_batchruntomo, EtomoOutput
from .utils.installation import check_imod_installation


def align_tilt_series_using_fiducials(
        tilt_series: np.ndarray,
        tilt_angles: List[float],
        pixel_size: float,
        fiducial_size: float,
        nominal_rotation_angle: float,
        basename: str,
        output_directory: Path,
        skip_if_completed: bool = False
) -> EtomoOutput:
    """Run fiducial based alignment in IMOD on a single tilt-series.

    Parameters
    ----------
    tilt_series: (n, y, x) array of 2D tilt-images in a tilt-series.
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: nominal pixel size in Angstroms per pixel.
    fiducial_size: approximate size of fiducials in nanometers.
    nominal_rotation_angle: initial estimate for the rotation angle of the tilt
        axis. https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    basename: basename for files in Etomo directory.
    skip_if_completed: skip alignment if previous results found.
    output_directory: tilt-series directory for IMOD.
    """
    check_imod_installation()
    output_directory = Path(output_directory)
    etomo_output = prepare_etomo_directory(
        directory=output_directory,
        tilt_series=tilt_series,
        tilt_angles=tilt_angles,
        basename=basename,

    )
    directive = generate_alignment_directive(
        tilt_series_file=etomo_output.tilt_series_file,
        pixel_size=pixel_size,
        fiducial_size=fiducial_size,
        rotation_angle=nominal_rotation_angle
    )
    if etomo_output.contains_alignment_results is False or skip_if_completed is False:
        run_batchruntomo(
            directory=output_directory,
            basename=basename,
            directive=directive
        )
        if etomo_output.contains_alignment_results is False:
            raise RuntimeError(f'{basename} failed to align correctly.')
    return etomo_output


def generate_alignment_directive(
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
    directive['setupset.copyarg.rotation'] = str(rotation_angle)
    directive['setupset.copyarg.pixel'] = str(pixel_size / 10)
    directive['setupset.copyarg.gold'] = str(fiducial_size)
    directive['comparam.prenewst.newstack.BinByFactor'] = str(alignment_binning_factor)
    return directive
