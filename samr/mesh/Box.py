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


# --- Class definition

class Box:
    """
    The Box class defines a rectangular region of index space.
    """
    # --- Properties

    @property
    def lower(self):
        """
        numpy.ndarray: lower corner of index space covered by Box

        Notes
        -----
        * lower.dtype = 'int64'
        """
        return self._lower

    @property
    def upper(self):
        """
        numpy.ndarray: upper corner of index space covered by Box

        Notes
        -----
        * upper.dtype = 'int64'
        """
        return self._upper

    @property
    def num_dimensions(self):
        """
        int: dimensionality of Box
        """
        return len(self.lower)

    @property
    def shape(self):
        """
        tuple: number of cells Box has in each coordinate direction
        """
        return self._shape

    @property
    def size(self):
        """
        int: number of cells in Box
        """
        return self._size

    # --- Public methods

    def __init__(self, lower, upper):
        """
        Initialize Box.

        Parameters
        ----------
        lower: list, tuple, or numpy.ndarray
            lower corner of index space covered by Box

        upper: list, tuple, or numpy.ndarray
            upper corner of index space covered by Box

        Examples
        --------
        >>> lower = [0, 0, 0]
        >>> upper = [9, 9, 9]
        >>> box = Box(lower, upper)
        >>> box.num_dimensions
        3
        >>> box.shape
        (10, 10, 10)
        >>> box.size
        1000
        """
        # --- Check arguments

        # lower
        if not isinstance(lower, (list, tuple, numpy.ndarray)):
            raise ValueError("'lower' is not a list, tuple, or numpy.ndarray")

        # lower contains only integer values
        if not Box._contains_only_integers(lower):
            raise ValueError("'lower' contains non-integer values")

        # upper
        if not isinstance(upper, (list, tuple, numpy.ndarray)):
            raise ValueError("'upper' is not a list, tuple, or numpy.ndarray")

        # upper contains only integer values
        if not Box._contains_only_integers(upper):
            raise ValueError("'upper' contains non-integer values")

        # len(lower) == len(upper)
        if len(lower) != len(upper):
            raise ValueError("'lower' and 'upper' do not have the same "
                             "number of components")

        # upper >= lower
        if not numpy.all(numpy.greater_equal(upper, lower)):
            raise ValueError("Some components of 'upper' are less than "
                             "components of 'lower'")

        # --- Set property and attribute values

        # index space
        self._lower = numpy.array(lower, dtype='int64')
        self._upper = numpy.array(upper, dtype='int64')

        # shape
        self._shape = tuple(self.upper - self.lower +
                            numpy.ones(self.num_dimensions, dtype='int64'))

        # size
        self._size = numpy.product(self.shape)

    # --- Private methods

    @staticmethod
    def _contains_only_integers(array):
        """
        Return whether 'array' contains only integer values.

        Parameters
        ----------
        array: scalar or array-like (e.g., list, tuple, numpy.array)
            array of values to evaluate

        Return value
        ------------
        bool: True if 'array' contains only integer values; False otherwise

        Examples
        --------
        >>> array = [0.0, 1.0, 2.0]
        >>> Box._contains_only_integers(array)
        True
        >>> array = [0.5, 1.0, 2.0]
        >>> Box._contains_only_integers(array)
        False
        >>> array = numpy.array([0, 1, 2])
        >>> Box._contains_only_integers(array)
        True
        >>> array = numpy.ones(10)
        >>> Box._contains_only_integers(array)
        True
        >>> Box._contains_only_integers(3)
        True
        >>> Box._contains_only_integers(3.5)
        False
        """
        return numpy.all(numpy.equal(numpy.mod(array, 1), 0))
