from pathlib import Path

import numpy as np

from yet_another_imod_wrapper.fiducials import align_tilt_series_using_fiducials

TEST_DATA_DIR = Path(__file__).parent.parent / 'tilt_series'

align_tilt_series_using_fiducials(
    tilt_series_file=TEST_DATA_DIR / 'my_prefix_TS_01.mrc',
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    fiducial_size=10,
    nominal_rotation_angle=85,
    output_directory=Path('test_TS_01_fiducials')
)
