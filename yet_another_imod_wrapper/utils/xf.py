import os

import numpy as np
from .io import read_xf


class XF:
    """Convenient retrieval of properties from IMOD xf data."""

    def __init__(self, xf: np.ndarray):
        self.xf_data = xf

    @classmethod
    def from_file(cls, filename: os.PathLike):
        return cls(read_xf(filename))

    @property
    def shifts(self):
        """Post-transformation shifts directly from xf data.

        Output is an (n, 2) numpy array of XY shifts. Shifts in an xf file are
        applied after rotations. IMOD xf files contain linear transformations. In
        the context of tilt-series alignment they contain transformations which are
        applied to 'align' a tilt-series such that images represent a fixed body rotating
        around the Y-axis.
        """
        return self.xf_data[:, -2:]

    @property
    def transformation_matrices(self):
        """2D transformation matrices directly from xf data.

        Output is an (n, 2, 2) numpy array of matrices.
        """
        return self.xf_data[:, :4].reshape((-1, 2, 2))

    @property
    def in_plane_rotations(self):
        """Extract the in plane rotation angle from IMOD xf data.

        Output is an (n, ) numpy array of angles in degrees. This assumes
        that the transformation in the xf file is a simple 2D rotation.
        """
        cos_theta = self.transformation_matrices[:, 0, 0]
        return np.rad2deg(np.arccos(cos_theta))

    @property
    def image_shifts(self):
        """Shifts to align tilt-images with projected specimen.

        Rotation center is in IMOD convention (N-1) / 2.
        """
        inverse_transformation_matrices = np.linalg.pinv(self.transformation_matrices)
        return np.squeeze(inverse_transformation_matrices @ self.shifts.reshape((-1, 2, 1)))

    @property
    def specimen_shifts(self):
        """Shifts which align projected specimen with tilt-images.

        Rotation center is in IMOD convention (N-1) / 2.
        """
        return -self.image_shifts
