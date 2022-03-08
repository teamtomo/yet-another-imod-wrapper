from os import PathLike
from typing import Dict


def read_adoc(adoc_file: PathLike) -> Dict[str, str]:
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
    with open(output_filename, 'w') as adoc:
        for k, v in data.items():
            adoc.write(f"{k} = {v}\n")
