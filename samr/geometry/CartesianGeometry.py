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
from . import Geometry

# --- Constants


# --- Class definition

class CartesianGeometry(Geometry):
    """
    CartesianGeometry provides support for relating rectangular regions of
    index space to regions of a Cartesian coordinate space.

    * logically rectangular region of space
    * uniform grid spacing in each direction
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
        numpy.ndarray: lower corner of mesh
        """
        return self._x_lower

    @property
    def dx(self):
        """
        numpy.ndarray: grid spacing of mesh
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

        x_lower: numpy.ndarray
            lower corner of mesh

        dx: numpy.ndarray
            grid spacing of mesh

        Examples
        --------
        >>> num_dimensions = 3
        >>> x_lower = numpy.array([1, 2, 3])
        >>> dx = 0.1 * numpy.ones(num_dimensions)
        >>> geometry = CartesianGeometry(num_dimensions, x_lower, dx)
        >>> geometry.num_dimensions
        3
        >>> geometry.x_lower
        array([1., 2., 3.])
        >>> geometry.dx
        array([0.1, 0.1, 0.1])
        """
        # --- Call super()

        super().__init__(num_dimensions)

        # --- Check arguments

        # x_lower
        if not isinstance(x_lower, numpy.ndarray):
            raise ValueError("'x_lower' is not a numpy.ndarray")

        if len(x_lower) != num_dimensions:
            err_msg = "'x_lower' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        # dx
        if not isinstance(dx, numpy.ndarray):
            raise ValueError("'dx' is not a numpy.ndarray")

        if len(dx) != num_dimensions:
            err_msg = "'dx' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        if not numpy.all(numpy.greater(dx, numpy.zeros(num_dimensions))):
            raise ValueError("'dx' contains a non-positive value")

        # --- Set property and attribute values

        self._num_dimensions = num_dimensions
        self._x_lower = x_lower.astype('float64')
        self._dx = dx.astype('float64')
