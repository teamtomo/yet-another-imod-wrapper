import subprocess
import tempfile
from pathlib import Path
from typing import Sequence, List, Dict, Union

import mrcfile
import numpy as np

from .io import write_adoc


class EtomoOutput:
    def __init__(self, basename: str, directory: Path):
        self.directory: Path = directory
        self.basename: str = basename

    @property
    def tilt_series_file(self) -> Path:
        return self.directory / f'{self.basename}.mrc'

    @property
    def rawtlt_file(self) -> Path:
        return self.directory / f'{self.basename}.rawtlt'

    @property
    def xf_file(self) -> Path:
        return self.directory / f'{self.basename}.xf'

    @property
    def tlt_file(self) -> Path:
        return self.directory / f'{self.basename}.tlt'

    @property
    def edf_file(self) -> Path:
        return self.directory / f'{self.basename}.edf'

    @property
    def align_log_file(self) -> Path:
        return self.directory / 'align.log'

    @property
    def is_ready_for_alignment(self) -> bool:
        return self.tilt_series_file.exists() and self.rawtlt_file.exists()

    @property
    def contains_alignment_results(self) -> bool:
        return self.xf_file.exists() and self.tlt_file.exists()


def prepare_etomo_directory(
        directory: Path,
        tilt_series: np.ndarray,
        tilt_angles: Sequence[float],
        basename: str,
) -> EtomoOutput:
    """Prepare a directory for IMOD tilt-series alignment."""
    directory.mkdir(exist_ok=True, parents=True)
    output = EtomoOutput(basename=basename, directory=directory)
    tilt_series_file = output.tilt_series_file
    data_on_disk_shape = None
    if tilt_series_file.exists():
        with mrcfile.open(tilt_series_file, header_only=True) as mrc:
            data_on_disk_shape = (mrc.header.nz, mrc.header.ny, mrc.header.nx)
    if not np.array_equal(tilt_series.shape, data_on_disk_shape):
        mrcfile.write(
            tilt_series_file,
            tilt_series.astype(np.float32),
            overwrite=True
        )
    np.savetxt(output.rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')
    return output


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
        with open(directory / 'log.txt', mode='w') as log:
            subprocess.run(batchruntomo_command, stdout=log, stderr=log)


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


def get_tilt_angle_offset(align_log_file: Path) -> Union[float, None]:
    """Get the total tilt angle offset from an align.log file."""
    with open(align_log_file, mode='r') as file:
        for line in file:
            if 'Total tilt angle change =' in line:
                return float(line.strip().split('=')[-1])
    return None

