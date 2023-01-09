# Command-Line

```sh
$ yet-another-imod-wrapper fiducials
```

```txt                                                                        
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