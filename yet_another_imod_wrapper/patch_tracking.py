import subprocess
from os import PathLike
from pathlib import Path
from typing import Dict, Any, Tuple
import tempfile

from .constants import TARGET_PIXEL_SIZE_FOR_ALIGNMENT, BATCHRUNTOMO_CONFIG_PATCH_TRACKING
from .utils import find_optimal_power_of_2_binning_factor
from .batchruntomo_config.io import read_adoc, write_adoc


def batchruntomo_patch_tracking(
        tilt_series_file: PathLike,
        pixel_size: float,
        rotation_angle: float,
        patch_size_xy: Tuple[int, int],
        patch_overlap_percentage: float
):
    """Run IMOD tilt-series alignment on a single tilt-series.

    Tilt-series should be in its own directory with an associated text file
    containing the raw tilt-angles, one per line.
    e.g. TS_01/TS_01.mrc and TS_01/TS_01.rawtlt

    Parameters
    ----------
    tilt_series_file: file containing tilt-series images
        File must be compatible with the version of IMOD installed.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    rotation_angle: initial estimate for the rotation angle
        https://bio3d.colorado.edu/imod/doc/tomoguide.html#UnknownAxisAngle
    patch_size_xy: size of patches to be tracked in the unbinned tilt-series
    patch_overlap_percentage: overlap between patches in each direction.
        e.g. 33 for 33% overlap in each direction.
    """
    tilt_series_directory = Path(tilt_series_file).parent
    root_name = Path(tilt_series_file).stem
    directive = generate_patch_tracking_alignment_directive(
        tilt_series_file=tilt_series_file,
        pixel_size=pixel_size,
        rotation_angle=rotation_angle,
        patch_size_xy=patch_size_xy,
        patch_overlap_percentage=patch_overlap_percentage,
    )
    with tempfile.TemporaryDirectory() as temporary_directory:
        directive_file = Path(temporary_directory) / 'directive.adoc'
        write_adoc(directive, directive_file)
        batchruntomo_command = [
            'batchruntomo',
            '-DirectiveFile', f'{directive_file}',
            '-RootName', f'{root_name}',
            '-CurrentLocation', f'{tilt_series_directory}',
            '-EndingStep', '6'
        ]
        subprocess.run(batchruntomo_command)


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
    tilt_series_file : file containing the tilt-series stack
    pixel_size : pixel size in the tilt-series (angstroms per pixel)
    fiducial_size : fiducial size (nanometers)
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
    directive['setupset.copyarg.rotation'] = rotation_angle
    directive['setupset.copyarg.pixel'] = pixel_size / 10
    directive['comparam.prenewst.newstack.BinByFactor'] = alignment_binning_factor
    directive['comparam.xcorr_pt.tiltxcorr.OverlapOfPatchesXandY'] = f'{patch_overlap_factor},' \
                                                                     f'{patch_overlap_factor}'
    directive['comparam.xcorr_pt.tiltxcorr.SizeOfPatchesXandY'] = f'{patch_size_xy_binned[0]},' \
                                                                  f'{patch_size_xy_binned[1]}'

    return directive
