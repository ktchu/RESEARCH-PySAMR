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
from abc import ABC

# XYZ
from samr import utils


# --- Class definition

class Geometry(ABC):
    """
    A Geometry represents a region of coordinate space. It defines the
    relationship between a rectangular region of index space and a rectangular
    region of coordinate space.

    The Geometry class is a base class for subclasses that represent specific
    coordinate spaces.

    The Geometry class manages the following properties that are common to
    all coordinate spaces:

    - num_dimensions: dimensionality of space
    """
    # pylint: disable=too-few-public-methods

    # --- Properties

    @property
    def num_dimensions(self):
        """
        int: number of spatial dimensions
        """
        return self._num_dimensions

    # --- Public methods

    def __init__(self, num_dimensions):
        """
        Initialize Geometry.

        Parameters
        ----------
        num_dimensions: int
            number of spatial dimensions

        Examples
        --------
        >>> geometry = Geometry(num_dimensions=3)
        """
        # --- Check arguments

        # num_dimensions is a real-valued scalar
        if not utils.is_scalar(num_dimensions):
            raise ValueError("'num_dimensions' should be a numeric value")

        # num_dimensions is an integer value
        if num_dimensions % 1 != 0:
            raise ValueError("'num_dimensions' should be an integer")

        # num_dimensions > 0
        if num_dimensions <= 0:
            raise ValueError("'num_dimensions' should be a positive number")

        # --- Initialize property and attribute values

        self._num_dimensions = num_dimensions

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
        >>> geometry = Geometry(8)
        >>> print(geometry)
        Geometry(8)
        """
        return "Geometry({})".format(self.num_dimensions)

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
        >>> geometry = Geometry(8)
        >>> equivalent_geometry = Geometry(8)
        >>> geometry == equivalent_geometry
        True
        >>> geometry is equivalent_geometry
        False
        """
        if isinstance(other, self.__class__):
            return self.num_dimensions == other.num_dimensions

        return False
