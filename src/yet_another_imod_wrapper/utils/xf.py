import os
from typing import Optional
from warnings import warn

import numpy as np
from .io import read_xf


class XF:
    """Convenient retrieval of properties from IMOD xf data.

    An xf file contains one line with six numbers per image in the tilt-series,
    each specifying a linear transformation:

        A11 A12 A21 A22 DX DY

    where the coordinate `(X, Y)` is transformed to `(X', Y')` by:

        X' = A11 * X + A12 * Y + DX
        Y' = A21 * X + A22 * Y + DY

    The rotation center in IMOD is at `(N-1) / 2` where `N` is the
    number of elements in each dimension. This calculates a 0-indexed
    coordinate.
    """

    def __init__(
        self,
        xf: np.ndarray,
        initial_tilt_axis_rotation_angle: Optional[float] = None
    ):
        self.xf_data = xf
        self.initial_tilt_axis_rotation_angle = initial_tilt_axis_rotation_angle

    @classmethod
    def from_file(
        cls,
        filename: os.PathLike,
        initial_tilt_axis_rotation_angle: float = None
    ):
        return cls(read_xf(filename), initial_tilt_axis_rotation_angle)

    @property
    def shifts(self) -> np.ndarray:
        """`(n, 2)` array of `(DX, DY)` from xf data.

        These shifts are applied **after** rotation/skew.
        """
        return self.xf_data[:, -2:]

    @property
    def transformation_matrices(self) -> np.ndarray:
        """`(n, 2, 2)` array containing `A11, A12, A21, A22` from xf data."""
        return self.xf_data[:, :4].reshape((-1, 2, 2))

    @property
    def in_plane_rotations(self) -> np.ndarray:
        """`(n, )` array of in plane rotation angles from xf data.

        Angles are in degrees and counter-clockwise angles are positive.
        """
        cos_theta = self.transformation_matrices[:, 0, 0]
        theta = np.rad2deg(np.arccos(cos_theta))
        if self.initial_tilt_axis_rotation_angle is None:
            warn(
                'no initial value provided for tilt-axis angle was \
                provided and there are multiple valid solutions  \
                for the requested in-plane rotation angle.'
            )
        else:
            initial_theta = self.initial_tilt_axis_rotation_angle
            difference = np.abs(initial_theta - theta).sum()
            flipped_difference = np.abs((-1 * initial_theta) - theta).sum()
            if flipped_difference < difference:
                theta = -1 * theta
        return theta

    @property
    def image_shifts(self) -> np.ndarray:
        """`(n, 2)` array of xy shifts aligning tilt-images with the projected specimen.

        Rotation center is in IMOD convention `(N-1) / 2`.
        """
        inverse_transformation_matrices = np.linalg.pinv(self.transformation_matrices)
        return np.squeeze(inverse_transformation_matrices @ self.shifts.reshape((-1, 2, 1)))

    @property
    def specimen_shifts(self) -> np.ndarray:
        """`(n, 2)` array of xy shifts aligning the projected specimen with tilt-images.

        Rotation center is in IMOD convention `(N-1) / 2`.
        """
        return -self.image_shifts
