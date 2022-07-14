from pathlib import Path

import numpy as np
import mrcfile

from yet_another_imod_wrapper import align_tilt_series_using_fiducials

TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'

align_tilt_series_using_fiducials(
    tilt_series=mrcfile.read(TEST_DATA_DIR / 'TS_01.mrc'),
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    fiducial_size=10,
    nominal_rotation_angle=85,
    basename='TS_01',
    output_directory=Path('test_TS_01_fiducials')
)
