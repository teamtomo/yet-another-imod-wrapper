# yet-another-imod-wrapper

[![License](https://img.shields.io/pypi/l/yet-another-imod-wrapper.svg?color=green)](https://github.com/alisterburt/yet-another-imod-wrapper/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/yet-another-imod-wrapper.svg?color=green)](https://pypi.org/project/yet-another-imod-wrapper)
[![Python Version](https://img.shields.io/pypi/pyversions/yet-another-imod-wrapper.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/yet-another-imod-wrapper/actions/workflows/ci.yml/badge.svg)](https://github.com/alisterburt/yet-another-imod-wrapper/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/alisterburt/yet-another-imod-wrapper/branch/main/graph/badge.svg)](https://codecov.io/gh/alisterburt/yet-another-imod-wrapper)

A simple Python API for aligning single axis tilt-series in IMOD.

```python
from yet_another_imod_wrapper import (
    align_tilt_series_using_fiducials, 
    align_tilt_series_using_patch_tracking
)
import mrcfile
import numpy as np

# load tilt series into (n, y, x) numpy array
tilt_series = mrcfile.read('my_tilt_series.mrc')

# align using fiducials
align_tilt_series_using_fiducials(
    tilt_series=tilt_series,
    tilt_angles=np.arange(-60, 63, 3),
    pixel_size=1.35,
    fiducial_size=10,
    nominal_rotation_angle=85,
    basename='my_tilt_series',
    output_directory='fiducials',
    skip_if_completed=False
)

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


## Installation

This package requires that `IMOD>=4.11.0` is installed and on the `PATH`.

`yet-another-imod-wrapper` can be installed using `pip`. 

```shell
pip install yet-another-imod-wrapper
```

We recommend installing into a fresh virtual environment.
