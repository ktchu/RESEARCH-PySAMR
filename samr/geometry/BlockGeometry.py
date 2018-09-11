"""
TODO: add docstring

------------------------------------------------------------------------------
COPYRIGHT/LICENSE.  This file is part of the XYZ package.  It is subject
to the license terms in the LICENSE file found in the top-level directory of
this distribution.  No part of the XYZ package, including this file, may be
copied, modified, propagated, or distributed except according to the terms
contained in the LICENSE file.
------------------------------------------------------------------------------
"""
# pylint: disable=invalid-name

# --- Imports

# Standard library

# External packages
import numpy

# XYZ
# TODO

# --- Constants


# --- Class definition

class BlockGeometry:
    """
    TODO
    """
    # --- Properties

    @property
    def num_dimensions(self):
        """
        int: number of spatial dimensions
        """
        return self._num_dimensions

    @property
    def x_lower(self):
        """
        numpy.array: lower corner of MeshBlock
        """
        return self._x_lower

    @property
    def dx(self):
        """
        numpy.array: grid spacing on MeshBlock
        """
        return self._dx

    # --- Public methods

    def __init__(self, num_dimensions, x_lower, dx):
        """
        TODO

        Parameters
        ----------
        num_dimensions: int
            number of spatial dimensions

        x_lower: numpy.array
            lower corner of MeshBlock

        dx: numpy.array
            grid spacing on MeshBlock

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # num_dimensions
        if not isinstance(num_dimensions, int):
            raise ValueError("'num_dimensions' is not an integer")

        if num_dimensions <= 0:
            raise ValueError("'num_dimensions' is not a positive integer")

        # x_lower
        if not isinstance(x_lower, numpy.array):
            raise ValueError("'x_lower' is not a numpy.array")

        if len(x_lower) != num_dimensions:
            err_msg = "'x_lower' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        # dx
        if not isinstance(dx, numpy.array):
            raise ValueError("'dx' is not a numpy.array")

        if len(dx) != num_dimensions:
            err_msg = "'dx' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        # --- Set property and attribute values

        self._num_dimensions = num_dimensions
        self._x_lower = x_lower
        self._dx = dx
