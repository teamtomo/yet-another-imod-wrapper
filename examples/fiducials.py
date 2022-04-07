from pathlib import Path

import numpy as np

from yet_another_imod_wrapper.fiducials import run_fiducial_based_alignment

TEST_DATA_DIR = Path(__file__).parent.parent / 'tilt_series'

run_fiducial_based_alignment(
    tilt_series_file=TEST_DATA_DIR / 'TS_01.mrc',
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    fiducial_size=10,
    nominal_rotation_angle=85,
    output_directory=Path('test_TS_01_fiducials')
)
