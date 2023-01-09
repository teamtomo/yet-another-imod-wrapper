"""Command line interface for fiducial and patch-tracking based alignments."""
from pathlib import Path
from typing import Optional

import typer
import mrcfile

from .fiducials import align_tilt_series_using_fiducials
from .patch_tracking import align_tilt_series_using_patch_tracking
from .utils.io import read_tlt

cli = typer.Typer(add_completion=False, no_args_is_help=True)


@cli.command(name='fiducials')
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
        ..., help='in-plane rotation of tilt-axis away from the Y-axis, CCW positive.'
    ),
    basename: Optional[str] = typer.Option(
        default=None, help='basename for files in output directory.'
    )

):
    basename = tilt_series.stem if basename is None else basename
    tilt_series = mrcfile.read(tilt_series)
    tilt_angles = read_tlt(tilt_angles)
    output_directory.mkdir(parents=True, exist_ok=True)
    align_tilt_series_using_fiducials(
        tilt_series=tilt_series,
        tilt_angles=tilt_angles,
        pixel_size=pixel_size,
        fiducial_size=fiducial_size,
        nominal_rotation_angle=nominal_rotation_angle,
        basename=basename,
    )
