# Overview

This package aims to provide a simple API for aligning tilt-series using 
[IMOD](https://bio3d.colorado.edu/imod/) in Python and from the command-line.

<figure markdown>
<p align="center" width="100%">
    <img width="60%" src="https://user-images.githubusercontent.
com/7307488/211384589-18d91111-ef31-4e7a-836b-4580cb602249.png">
</p>
  <figcaption>Tilt-series alignment models how a 3D specimen 
is projected into 2D. Reproduced from <a href="https://doi.org/10.
1007/978-0-387-69008-7_6">a paper by David 
Mastronarde</a>.</figcaption>
</figure>

## Why does this package exist?

IMOD is a powerful software package with a 
[huge API surface](https://bio3d.colorado.edu/imod/#Guides).
Setting up
[batchruntomo](https://bio3d.colorado.edu/imod/doc/batchGuide.html)
can be tricky for those unfamiliar with IMOD and taking the results into downstream 
tools for further processing requires a deep understanding of IMOD's metadata model.

Covering only the use cases of single-axis cryo-TEM tilt-series alignment, 
this package aims to provide a simple way to align tilt-series and work with IMOD 
metadata for cryo-ET practitioners more familiar with Python and shell scripting 
than IMOD.

## Usage

I want to...

- [align a tilt-series with fiducials in Python](./fiducials/python.md)
- [align a tilt-series with patch-tracking in Python](./patch-tracking/python.md)
- [align a tilt-series with fiducials from the command-line](./fiducials/python.md)
- [align a tilt-series with patch-tracking from the command-line](./patch-tracking/cli.md)
- [work with IMOD metadata in Python](metadata/handlers.md)

## Further reading

- [IMOD tomography guide](https://bio3d.colorado.edu/imod/doc/tomoguide.html)
- [Fiducial Marker and Hybrid Alignment Methods for Single- and Double-axis Tomography](http://dx.doi.org/10.1007/978-0-387-69008-7_6)
