"""Command line interface for fiducial and patch-tracking based alignments."""
from pathlib import Path
from typing import Optional

import typer
import mrcfile

from .fiducials import align_tilt_series_using_fiducials
from .patch_tracking import align_tilt_series_using_patch_tracking
from .utils.io import read_tlt

cli = typer.Typer(
    name='yet-another-imod-wrapper',
    help="A simple command line interface for automated tilt-series alignment using "
         "IMOD",
    add_completion=False,
    no_args_is_help=True
)


@cli.command(no_args_is_help=True)
def fiducials(
    tilt_series: Path = typer.Option(
        ..., help='file containing tilt-series in MRC format.'
    ),
    tilt_angles: Path = typer.Option(
        ..., help='text file containing tilt-angles, one per line.'
    ),
    output_directory: Path = typer.Option(..., help='directory for IMOD output.'),
    pixel_size: float = typer.Option(..., help='pixel spacing in Ångstroms.'),
    fiducial_size: float = typer.Option(..., help='fiducial diameter in nanometers.'),
    nominal_rotation_angle: float = typer.Option(
        ..., help='in-plane rotation of tilt-axis away from the Y-axis in degrees, '
                  'CCW positive.'
    ),
    basename: Optional[str] = typer.Option(
        default=None, help='basename for files in output directory.'
    )

):
    basename = tilt_series.stem if basename is None else basename
    tilt_series = mrcfile.read(tilt_series)
    tilt_angles = read_tlt(tilt_angles)
    align_tilt_series_using_fiducials(
        tilt_series=tilt_series,
        tilt_angles=tilt_angles,
        pixel_size=pixel_size,
        fiducial_size=fiducial_size,
        nominal_rotation_angle=nominal_rotation_angle,
        basename=basename,
        output_directory=output_directory,
    )


@cli.command(no_args_is_help=True)
def patch_tracking(
    tilt_series: Path = typer.Option(
        ..., help='file containing tilt-series in MRC format.'
    ),
    tilt_angles: Path = typer.Option(
        ..., help='text file containing tilt-angles, one per line.'
    ),
    output_directory: Path = typer.Option(..., help='directory for IMOD output.'),
    pixel_size: float = typer.Option(..., help='pixel spacing in Ångstroms.'),
    patch_size: float = typer.Option(
        default=1000, help='patch sidelength in Ångstroms.'
    ),
    patch_overlap_percentage: float = typer.Option(
        default=33, help='percentage of tile-length to overlap on each side.'
    ),
    nominal_rotation_angle: float = typer.Option(
        ..., help='in-plane rotation of tilt-axis away from the Y-axis in degrees, '
                  'CCW positive.'
    ),
    basename: Optional[str] = typer.Option(
        default=None, help='basename for files in output directory.'
    )
):
    basename = tilt_series.stem if basename is None else basename
    tilt_series = mrcfile.read(tilt_series)
    tilt_angles = read_tlt(tilt_angles)
    align_tilt_series_using_patch_tracking(
        tilt_series=tilt_series,
        tilt_angles=tilt_angles,
        nominal_rotation_angle=nominal_rotation_angle,
        pixel_size=pixel_size,
        patch_size=patch_size,
        patch_overlap_percentage=patch_overlap_percentage,
        basename=basename,
        output_directory=output_directory,
    )