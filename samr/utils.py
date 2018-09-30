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


# --- Public module functions

def array_is_empty(array):
    """
    Return whether 'array' is empty.

    Parameters
    ----------
    array: list, tuple, or numpy.array
        array of values to evaluate

    Return value
    ------------
    bool: True if 'array' is empty; False otherwise

    Examples
    --------
    >>> array_is_empty([])
    True
    >>> array_is_empty(tuple([]))
    True
    >>> array_is_empty(numpy.array([]))
    True
    >>> array_is_empty([0, 1, 2])
    False
    """
    # --- Check arguments

    if not isinstance(array, (list, tuple, numpy.ndarray)):
        raise ValueError("'array' is not a list, tuple, or numpy.ndarray")

    # --- Determine if array is empty

    # 'array' is an numpy.ndarray
    if isinstance(array, numpy.ndarray):
        return array.size == 0

    # 'array' is a list or tuple
    return not array


def contains_only_integers(array):
    """
    Return whether 'array' is non-empty and contains only integer values.

    Parameters
    ----------
    array: scalar (int or float) or array-like (list, tuple, or numpy.array)
        array of values to evaluate

    Return value
    ------------
    bool: True if 'array' is non-empty contains only integer values;
        False otherwise

    Examples
    --------
    >>> contains_only_integers([0, 1, 2])
    True
    >>> contains_only_integers(3)
    True
    >>> contains_only_integers(numpy.array([0, 1, 2]))
    True
    >>> contains_only_integers([0.0, 1.0, 2.0])
    True
    >>> contains_only_integers([0.5, 1.0, 2.0])
    False
    >>> contains_only_integers(3.5)
    False
    >>> contains_only_integers([])
    False
    """
    # --- Check arguments

    if not isinstance(array, (int, float, list, tuple, numpy.ndarray)):
        raise ValueError("'array' is not a scalar, list, tuple, or "
                         "numpy.ndarray")

    if isinstance(array, (list, tuple, numpy.ndarray)):
        try:
            _ = numpy.array(array, dtype=float)

        except Exception:
            raise ValueError("Unable to convert 'array' to an array of "
                             "numeric values")

        # Return False if 'array' is empty
        if isinstance(array, (list, tuple)):
            if not array:
                return False

        elif isinstance(array, numpy.ndarray):
            if array.size == 0:
                return False

    # --- Determine whether all entries of 'array' are integers

    return numpy.all(numpy.equal(numpy.mod(array, 1), 0))
