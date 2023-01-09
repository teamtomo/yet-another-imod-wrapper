import os
from os import PathLike
from typing import Dict

import numpy as np


def read_tlt(file: os.PathLike) -> np.ndarray:
    """Read an IMOD tlt file into an (n, ) numpy array."""
    return np.loadtxt(fname=file, dtype=float).reshape(-1)


def read_xf(file: os.PathLike) -> np.ndarray:
    """Read an IMOD xf file into an (n, 6) numpy array.

    The xf file with alignment transforms contains one
    line per view, each with a linear transformation specified by six numbers:
        A11 A12 A21 A22 DX DY
    where the coordinate (X, Y) is transformed to (X', Y') by:
        X' = A11 * X + A12 * Y + DX
        Y' = A21 * X + A22 * Y + DY
    """
    return np.loadtxt(fname=file, dtype=float).reshape((-1, 6))


def read_adoc(adoc_file: PathLike) -> Dict[str, str]:
    """Read an IMOD adoc file into a dictionary."""
    with open(adoc_file) as adoc:
        lines = adoc.readlines()
    lines = [
        line.strip().split('=')
        for line in lines
        if not line.startswith('#')
    ]
    lines = [line for line in lines if len(line) == 2]
    return {k.strip(): v.strip() for k, v in lines}


def write_adoc(data: dict, output_filename: PathLike):
    """Write an IMOD adoc file from a dictionary."""
    with open(output_filename, 'w') as adoc:
        for k, v in data.items():
            adoc.write(f"{k} = {v}\n")
