import subprocess
import tempfile
from pathlib import Path
from typing import Sequence, List, Dict

import mrcfile
import numpy as np

from yet_another_imod_wrapper.utils.io import write_adoc
from yet_another_imod_wrapper.etomo_directory import EtomoDirectory


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
