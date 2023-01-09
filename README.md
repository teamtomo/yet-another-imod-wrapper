# yet-another-imod-wrapper

[![License](https://img.shields.io/pypi/l/yet-another-imod-wrapper.svg?color=green)](https://github.com/alisterburt/yet-another-imod-wrapper/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/yet-another-imod-wrapper.svg?color=green)](https://pypi.org/project/yet-another-imod-wrapper)
[![Python Version](https://img.shields.io/pypi/pyversions/yet-another-imod-wrapper.svg?color=green)](https://python.org)
[![CI](https://github.com/alisterburt/yet-another-imod-wrapper/actions/workflows/test_and_deploy.yml/badge.svg)](https://github.com/alisterburt/yet-another-imod-wrapper/actions/workflows/test_and_deploy.yml)

A simple API for automated tilt-series alignment in IMOD.

## Usage

The package can be used from Python or the command line

### Python

#### Fiducials
```python
import mrcfile
import numpy as np
from yet_another_imod_wrapper import align_tilt_series_using_fiducials

# load tilt series into (n, y, x) numpy array
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

#### Patch-tracking
```python
import mrcfile
import numpy as np
from yet_another_imod_wrapper import align_tilt_series_using_patch_tracking

# load tilt series into (n, y, x) numpy array
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

### Command line

#### Fiducials
```sh
$ yet-another-imod-wrapper fiducials
                                                                                                                                                                                     
 Usage: yet-another-imod-wrapper fiducials [OPTIONS]                                                                                                                                 
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --tilt-series                   PATH   file containing tilt-series in MRC format. [default: None] [required]                                                                   │
│ *  --tilt-angles                   PATH   text file containing tilt-angles, one per line. [default: None] [required]                                                              │
│ *  --output-directory              PATH   directory for IMOD output. [default: None] [required]                                                                                   │
│ *  --pixel-size                    FLOAT  pixel spacing in Ångstroms. [default: None] [required]                                                                                  │
│ *  --fiducial-size                 FLOAT  fiducial diameter in nanometers. [default: None] [required]                                                                             │
│ *  --nominal-rotation-angle        FLOAT  in-plane rotation of tilt-axis away from the Y-axis in degrees, CCW positive. [default: None] [required]                                │
│    --basename                      TEXT   basename for files in output directory. [default: None]                                                                                 │
│    --help                                 Show this message and exit.                                                                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### Patch-tracking

```sh
$ yet-another-imod-wrapper patch-tracking
                                                                                                                                                                                     
 Usage: yet-another-imod-wrapper patch-tracking [OPTIONS]                                                                                                                            
                                                                                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --tilt-series                     PATH   file containing tilt-series in MRC format. [default: None] [required]                                                                 │
│ *  --tilt-angles                     PATH   text file containing tilt-angles, one per line. [default: None] [required]                                                            │
│ *  --output-directory                PATH   directory for IMOD output. [default: None] [required]                                                                                 │
│ *  --pixel-size                      FLOAT  pixel spacing in Ångstroms. [default: None] [required]                                                                                │
│    --patch-size                      FLOAT  patch sidelength in Ångstroms. [default: 500]                                                                                         │
│    --patch-overlap-percentage        FLOAT  percentage of tile-length to overlap on each side. [default: 33]                                                                      │
│ *  --nominal-rotation-angle          FLOAT  in-plane rotation of tilt-axis away from the Y-axis in degrees, CCW positive. [default: None] [required]                              │
│    --basename                        TEXT   basename for files in output directory. [default: None]                                                                               │
│    --help                                   Show this message and exit.                                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```



## Installation

This package requires that `IMOD>=4.11.0` is installed and on the `PATH`.

`yet-another-imod-wrapper` can be installed using `pip`. 

```shell
pip install yet-another-imod-wrapper
```

We recommend installing into a fresh virtual environment.
