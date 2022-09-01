from os import PathLike
from pathlib import Path
from typing import Dict, Any, Tuple, Sequence

import numpy as np

from .utils.io import read_adoc
from .constants import TARGET_PIXEL_SIZE_FOR_ALIGNMENT, BATCHRUNTOMO_CONFIG_PATCH_TRACKING
from .utils.installation import check_imod_installation
from .utils.binning import find_optimal_power_of_2_binning_factor
from .utils.etomo import prepare_etomo_directory, run_batchruntomo, EtomoOutput


def align_tilt_series_using_patch_tracking(
        tilt_series: np.ndarray,
        tilt_angles: Sequence[float],
        nominal_rotation_angle: float,
        pixel_size: float,
        patch_size: float,
        patch_overlap_percentage: float,
        basename: str,
        output_directory: Path,
        skip_if_completed: bool = False
) -> EtomoOutput:
    """Run patch-tracking alignment in IMOD on a single tilt-series.

    Parameters
    ----------
    tilt_series: (n, y, x) array of 2D tilt-images in a tilt-series.
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    nominal_rotation_angle: initial estimate for the rotation angle of the tilt
        axis. https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    patch_size: sidelength of patches to be tracked in angstroms.
    patch_overlap_percentage: overlap between patches in each direction.
        e.g. 33 for 33% overlap in each direction.
    basename: basename for IMOD files.
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
    patch_size_px = int(patch_size / pixel_size)
    directive = generate_patch_tracking_alignment_directive(
        tilt_series_file=etomo_output.tilt_series_file,
        pixel_size=pixel_size,
        rotation_angle=nominal_rotation_angle,
        patch_size_xy=(patch_size_px, patch_size_px),
        patch_overlap_percentage=patch_overlap_percentage,
    )
    if etomo_output.contains_alignment_results is False or skip_if_completed is False:
        run_batchruntomo(
            directory=output_directory,
            basename=basename,
            directive=directive,
        )
        if etomo_output.contains_alignment_results is False:
            raise RuntimeError(f'{basename} failed to align correctly.')
    return etomo_output


def generate_patch_tracking_alignment_directive(
        tilt_series_file: PathLike,
        pixel_size: float,
        rotation_angle: float,
        patch_size_xy: Tuple[int, int],
        patch_overlap_percentage: float,
) -> Dict[str, Any]:
    """Generate a fiducial-based alignment directive file for batchruntomo

    Parameters
    ----------
    tilt_series_file : file containing the tilt-series stack.
    pixel_size : pixel size in the tilt-series in Angstroms per pixel.
    fiducial_size : approximate fiducial size in nanometers.
    rotation_angle : initial estimate for the rotation angle
        https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    patch_size_xy: patch size in the unbinned tilt-series
    patch_overlap_percentage: overlap between patches in each direction.
        e.g. 33 for 33% overlap in each direction.
    """
    alignment_binning_factor = find_optimal_power_of_2_binning_factor(
        src_pixel_size=pixel_size, target_pixel_size=TARGET_PIXEL_SIZE_FOR_ALIGNMENT
    )
    patch_size_xy_binned = [int(s / alignment_binning_factor) for s in patch_size_xy]
    patch_overlap_factor = patch_overlap_percentage / 100

    directive = read_adoc(BATCHRUNTOMO_CONFIG_PATCH_TRACKING)
    directive['setupset.copyarg.stackext'] = Path(tilt_series_file).suffix
    directive['setupset.copyarg.rotation'] = str(rotation_angle)
    directive['setupset.copyarg.pixel'] = str(pixel_size / 10)
    directive['comparam.prenewst.newstack.BinByFactor'] = str(alignment_binning_factor)
    directive['comparam.xcorr_pt.tiltxcorr.OverlapOfPatchesXandY'] = f'{patch_overlap_factor},' \
                                                                     f'{patch_overlap_factor}'
    directive['comparam.xcorr_pt.tiltxcorr.SizeOfPatchesXandY'] = f'{patch_size_xy_binned[0]},' \
                                                                  f'{patch_size_xy_binned[1]}'

    return directive
