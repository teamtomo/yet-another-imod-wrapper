# Python

```python
import mrcfile
import numpy as np
from yet_another_imod_wrapper import align_tilt_series_using_patch_tracking

# load tilt series into (batch, h, w) numpy array
tilt_series = mrcfile.read('my_tilt_series.mrc')

# align using patch-tracking
align_tilt_series_using_patch_tracking(
    tilt_series=tilt_series,
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    patch_size=1000,
    patch_overlap_percentage=33,
    basename='my_tilt_series',
    output_directory='patch_tracking',
    skip_if_completed=False
)
```