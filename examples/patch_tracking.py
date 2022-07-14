from pathlib import Path

import mrcfile
import numpy as np

from yet_another_imod_wrapper import align_tilt_series_using_patch_tracking

TEST_DATA_DIR = Path(__file__).parent.parent / 'test_data'

align_tilt_series_using_patch_tracking(
    tilt_series=mrcfile.read(TEST_DATA_DIR / 'TS_01.mrc'),
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    nominal_rotation_angle=85,
    patch_size=1000,
    patch_overlap_percentage=33,
    basename='TS_01',
    output_directory=Path('test_TS_01_patch_tracking')
)
