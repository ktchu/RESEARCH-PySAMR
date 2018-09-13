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

# XYZ


# --- Constants


# --- Class definition

class Geometry:
    """
    Base class for classes that relate rectangular regions of index space
    to the continuous space TODO: better word choice.

    The base Geometry class manages properties that are common to all
    geometries:

    - num_dimensions: dimensionality of space

    Subclasses of Geometry should manage properties that are specific
    to the mapping of index space to ?? space.
    """
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
        TODO

        Parameters
        ----------
        num_dimensions: int
            number of spatial dimensions

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

        # --- Set property and attribute values

        self._num_dimensions = num_dimensions
