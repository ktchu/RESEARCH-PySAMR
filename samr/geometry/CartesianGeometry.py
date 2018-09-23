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
    A CartesianGeometry object represents a rectangular region of Cartesian
    coordinate space. It provides support for relating rectangular regions of
    index space to rectangular regions of a Cartesian coordinate space.

    TODO
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
        >>> x_lower = [0] * num_dimensions
        >>> dx = [0.1] * num_dimensions
        >>> geometry = CartesianGeometry(num_dimensions, x_lower, dx)
        >>> geometry.num_dimensions
        3
        >>> geometry.x_lower
        array([0., 0., 0.])
        >>> geometry.dx
        array([0.1, 0.1, 0.1])
        """
        # --- Call super()

        super().__init__(num_dimensions)

        # --- Check arguments

        # x_lower
        if not isinstance(x_lower, (list, tuple, numpy.ndarray)):
            raise ValueError("'x_lower' is not a list, tuple, or "
                             "numpy.ndarray")

        if len(x_lower) != num_dimensions:
            raise ValueError("'x_lower' does not have 'num_dimensions' "
                             "components")

        # dx
        if not isinstance(dx, (list, tuple, numpy.ndarray)):
            raise ValueError("'dx' is not a list, tuple, or numpy.ndarray")

        if len(dx) != num_dimensions:
            raise ValueError("'dx' does not have 'num_dimensions' components")

        if not numpy.all(numpy.greater(dx, numpy.zeros(num_dimensions))):
            raise ValueError("'dx' contains a non-positive value")

        # --- Set property and attribute values

        self._num_dimensions = num_dimensions
        self._x_lower = numpy.array(x_lower, dtype='float64')
        self._dx = numpy.array(dx, dtype='float64')

    # --- Magic methods

    def __eq__(self, other):
        """
        Return whether 'other' is an equivalent CartesianGeometry object.

        Parameters
        ----------
        other: object
            object to compare with

        Return value
        ------------
        bool: True if 'other' is an equivalent object; False otherwise

        Examples
        --------
        >>> num_dimensions = 3
        >>> x_lower = [0.0] * num_dimensions
        >>> dx = [0.1] * num_dimensions
        >>> geometry = CartesianGeometry(num_dimensions, x_lower, dx)
        >>> equivalent_geometry = \
                CartesianGeometry(num_dimensions, x_lower, dx)
        >>> geometry == equivalent_geometry
        True
        >>> geometry is equivalent_geometry
        False
        """
        if isinstance(other, self.__class__):
            return self.num_dimensions == other.num_dimensions and \
                   numpy.all(self.x_lower == other.x_lower) and \
                   numpy.all(self.dx == other.dx)

        return False
