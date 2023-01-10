# Command-Line

```sh
$ yet-another-imod-wrapper patch-tracking
```

```txt
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