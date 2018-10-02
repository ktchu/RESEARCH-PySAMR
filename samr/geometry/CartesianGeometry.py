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

# External packages
import numpy

# XYZ
from samr.box import Box  # pylint: disable=unused-import

from ..utils import is_array
from .Geometry import Geometry


# --- Class definition

class CartesianGeometry(Geometry):
    """
    A CartesianGeometry represents a rectangular region of Cartesian
    coordinate space. It maps rectangular regions of index space to a grid
    in Cartesian coordinate space that is uniform in each space dimension.
    """
    # --- Properties

    @property
    def x_lower(self):
        """
        numpy.ndarray: lower corner of region of Cartesian coordinate space

        Notes
        -----
        * x_lower.dtype = 'float64'
        """
        return self._x_lower

    @property
    def x_upper(self):
        """
        numpy.ndarray: upper corner of region of Cartesian coordinate space

        Notes
        -----
        * x_upper.dtype = 'float64'
        """
        return self._x_upper

    @property
    def shape(self):
        """
        numpy.ndarray: dimensions of region of Cartesian coordinate space

        Notes
        -----
        * shape.dtype = 'float64'
        """
        return self._shape

    # --- Public methods

    def __init__(self, x_lower, x_upper):
        """
        Initialize CartesianGeometry.

        Parameters
        ----------
        x_lower: list, tuple, or numpy.ndarray
            lower corner of region

        x_upper: list, tuple, or numpy.ndarray
            upper corner of region

        Examples
        --------
        >>> num_dimensions = 3
        >>> x_lower = [-1] * num_dimensions
        >>> x_upper = [1] * num_dimensions
        >>> geometry = CartesianGeometry(x_lower, x_upper)
        >>> geometry.num_dimensions
        3
        >>> geometry.x_lower
        array([-1., -1., -1.])
        >>> geometry.x_upper
        array([1., 1., 1.])
        >>> geometry.shape
        array([2., 2., 2.])
        """
        # --- Check arguments

        # x_lower
        if not is_array(x_lower):
            raise ValueError("'x_lower' should be a list, tuple, or "
                             "numpy.ndarray")

        # x_upper
        if not is_array(x_upper):
            raise ValueError("'x_upper' should be a list, tuple, or "
                             "numpy.ndarray")

        # len(x_lower) == len(x_upper)
        if len(x_lower) != len(x_upper):
            raise ValueError("'x_lower' and 'x_upper' should have the same "
                             "number of components")

        # x_upper > x_lower
        if not numpy.all(numpy.greater(x_upper, x_lower)):
            raise ValueError("'x_upper' should be greater than 'x_lower' "
                             "along all axes")

        # --- Call super()

        super().__init__(num_dimensions=len(x_lower))

        # --- Initialize property and attribute values

        # region bounds
        self._x_lower = numpy.array(x_lower, dtype='float64')
        self._x_upper = numpy.array(x_upper, dtype='float64')

        # shape
        self._shape = self.x_upper - self.x_lower

    def compute_geometry(self, reference_box, box):
        """
        Compute geometry for region of coordinate space covered by 'box'.

        Parameters
        ----------
        reference_box: Box
            box representing rectangular region of index space associated
            with 'self'

        box: Box
            box representing rectangular region of index space to compute
            geometry of

        Return values
        -------------
        Geometry: geometry of rectangular region of coordinate space covered
            by 'box'
        """
        # --- Check arguments

        # 'reference_box' and 'box' checked by Geometry.compute_geometry()
        super().compute_geometry(reference_box, box)

        # --- Compute geometry of region covered by 'box'

        dx = self.compute_dx(reference_box)

        x_lower = self.x_lower + dx * (box.lower - reference_box.lower)

        x_upper = self.x_upper + dx * (box.upper - reference_box.upper)

        return CartesianGeometry(x_lower, x_upper)

    def compute_dx(self, box):
        """
        Compute grid spacing.

        Parameters
        ----------
        box: Box
            box representing rectangular region of index space

        Return value
        ------------
        numpy.ndarray: grid spacing in each space dimension

        Examples
        --------
        >>> geometry = CartesianGeometry([0, 0], [10, 10])
        >>> box = Box([0, 0], [99, 99])
        >>> geometry.compute_dx(box)
        array([0.1, 0.1])
        """
        return self.shape / box.shape

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
        Return whether 'other' is an equivalent object.

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
