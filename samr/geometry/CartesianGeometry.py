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
    def x_lower(self):
        """
        numpy.ndarray: lower corner of mesh
        """
        return self._x_lower

    @property
    def x_upper(self):
        """
        numpy.ndarray: grid spacing of mesh
        """
        return self._x_upper

    # --- Public methods

    def __init__(self, x_lower, x_upper):
        """
        Initialize CartesianGeometry object.

        Parameters
        ----------
        x_lower: numpy.ndarray
            lower corner of mesh

        x_upper: numpy.ndarray
            upper corner of mesh

        Examples
        --------
        >>> num_dimensions = 3
        >>> x_lower = [0] * num_dimensions
        >>> x_upper = [1] * num_dimensions
        >>> geometry = CartesianGeometry(x_lower, x_upper)
        >>> geometry.num_dimensions
        3
        >>> geometry.x_lower
        array([0., 0., 0.])
        >>> geometry.x_upper
        array([1., 1., 1.])
        """
        # --- Check arguments

        # x_lower
        if not isinstance(x_lower, (list, tuple, numpy.ndarray)):
            raise ValueError("'x_lower' is not a list, tuple, or "
                             "numpy.ndarray")

        # x_upper
        if not isinstance(x_upper, (list, tuple, numpy.ndarray)):
            raise ValueError("'x_upper' is not a list, tuple, or "
                             "numpy.ndarray")

        # len(x_lower) == len(x_upper)
        if len(x_lower) != len(x_upper):
            raise ValueError("'x_lower' and 'x_upper' do not have the same "
                             "number of components")

        # x_upper > x_lower
        if not numpy.all(numpy.greater(x_upper, x_lower)):
            raise ValueError("'x_upper' less than or equal to 'x_lower' "
                             "along some axes")

        # --- Call super()

        super().__init__(num_dimensions=len(x_lower))

        # --- Set property and attribute values

        self._x_lower = numpy.array(x_lower, dtype='float64')
        self._x_upper = numpy.array(x_upper, dtype='float64')

    # --- Magic methods

    def __repr__(self):
        """
        Return unambiguous representation of object.

        Parameters
        ----------
        None

        Return value
        ------------
        str: unambiguous string representation of object

        Examples
        --------
        >>> geometry = CartesianGeometry([0, 0], [10, 10])
        >>> print(geometry)
        CartesianGeometry([0.0, 0.0], [10.0, 10.0])
        """
        return "CartesianGeometry({}, {})".format(list(self.x_lower),
                                                  list(self.x_upper))

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
        >>> x_upper = [1.0] * num_dimensions
        >>> geometry = CartesianGeometry(x_lower, x_upper)
        >>> equivalent_geometry = CartesianGeometry(x_lower, x_upper)
        >>> geometry == equivalent_geometry
        True
        >>> geometry is equivalent_geometry
        False
        """
        if isinstance(other, self.__class__):
            return self.num_dimensions == other.num_dimensions and \
                   numpy.all(self.x_lower == other.x_lower) and \
                   numpy.all(self.x_upper == other.x_upper)

        return False
