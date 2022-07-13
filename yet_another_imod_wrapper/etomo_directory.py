from pathlib import Path


class EtomoDirectory:
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
    def is_ready_for_alignment(self) -> bool:
        return self.tilt_series_file.exists() and self.rawtlt_file.exists()

    @property
    def contains_alignment_results(self) -> bool:
        return self.xf_file.exists() and self.tlt_file.exists()

