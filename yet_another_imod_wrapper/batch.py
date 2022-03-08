from os import PathLike
from typing import List, Tuple

from .fiducials import batchruntomo_fiducials
from .patch_tracking import batchruntomo_patch_tracking


def batch_alignment_fiducials(
        tilt_series_files: List[PathLike],
        pixel_size: float,
        fiducial_size: float,
        rotation_angle: float
):
    for tilt_series_file in tilt_series_files:
        batchruntomo_fiducials(
            tilt_series_file=tilt_series_file,
            pixel_size=pixel_size,
            fiducial_size=fiducial_size,
            rotation_angle=rotation_angle,
        )


def batch_alignment_patch_tracking(
        tilt_series_files: List[PathLike],
        pixel_size: float,
        rotation_angle: float,
        patch_size_xy: Tuple[int, int],
        patch_overlap_percentage: float
):
    for tilt_series_file in tilt_series_files:
        batchruntomo_patch_tracking(
            tilt_series_file=tilt_series_file,
            pixel_size=pixel_size,
            rotation_angle=rotation_angle,
            patch_size_xy=patch_size_xy,
            patch_overlap_percentage=patch_overlap_percentage
        )
