# Python

```python
import mrcfile
import numpy as np
from yet_another_imod_wrapper import align_tilt_series_using_fiducials

# load tilt series into (batch, h, w) numpy array
tilt_series = mrcfile.read('my_tilt_series.mrc')

# align using fiducials
output = align_tilt_series_using_fiducials(
    tilt_series=tilt_series,
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    fiducial_size=10,
    nominal_rotation_angle=85,
    basename='my_tilt_series',
    output_directory='fiducials',
    skip_if_completed=False
)
```