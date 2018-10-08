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
import abc

# XYZ
from samr.box import Box

from ..utils import is_scalar


# --- Class definition

class Geometry(abc.ABC):
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
        """
        # --- Check arguments

        # num_dimensions has expected type
        if not is_scalar(num_dimensions):
            raise ValueError("'num_dimensions' should be a numeric value")

        # num_dimensions is an integer value
        if num_dimensions % 1 != 0:
            raise ValueError("'num_dimensions' should be an integer")

        # num_dimensions > 0
        if num_dimensions <= 0:
            raise ValueError("'num_dimensions' should be a positive number")

        # --- Initialize property and attribute values

        self._num_dimensions = num_dimensions

    @abc.abstractmethod
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

        # reference_box has expected type
        if not isinstance(reference_box, Box):
            raise ValueError("'reference_box' should be a Box")

        # box has expected type
        if not isinstance(box, Box):
            raise ValueError("'box' should be a Box")

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
        """
        if isinstance(other, self.__class__):
            return self.num_dimensions == other.num_dimensions

        return False
