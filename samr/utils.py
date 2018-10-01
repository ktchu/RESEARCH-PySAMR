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
from collections.abc import Sequence

# External packages
import numpy


# --- Public module functions

def is_scalar(value, include_complex=False):
    """
    Return whether 'value' is a real-valued scalar.

    Parameters
    ----------
    value: object
        object to evaluate

    include_complex: bool
        when 'include_complex' is True, complex numbers are considered
        to be scalars. Otherwise, complex numbers are not considered to
        be scalars.

    Return value
    ------------
    bool: True if 'value' is a real-valued scalar; False otherwise

    Examples
    --------
    >>> is_scalar(1)
    True
    >>> is_scalar(1.3)
    True
    >>> is_scalar(1 + 1j)
    False
    >>> is_scalar(1 + 1j, include_complex=True)
    True
    >>> is_scalar([1, 2, 3])
    False
    >>> is_scalar(numpy.array([1.1])
    False
    """
    if include_complex:
        return isinstance(value, (int, float, complex))

    return isinstance(value, (int, float))


def is_array(array):
    """
    Return whether 'array' is a non-string array type.

    Parameters
    ----------
    array: object
        object to evaluate

    Return value
    ------------
    bool: True if 'array' is a non-string array type; False otherwise

    Examples
    --------
    >>> is_array([1, 2, 3])
    True
    >>> is_array(tuple([1, 2, 3]))
    True
    >>> is_array(numpy.array([1.1, 1.2, 1.3, 1.4]))
    True
    >>> is_array('string value')
    False
    """
    return isinstance(array, (Sequence, numpy.ndarray)) and \
        not isinstance(array, str)


def array_is_empty(array):
    """
    Return whether 'array' is empty.

    Parameters
    ----------
    array: non-string Sequence or numpy.array
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

    # 'array' is sequence-like but is not a string
    if not is_array(array):
        raise ValueError("'array' is not non-string Sequence or "
                         "a numpy.ndarray")

    # --- Determine if array is empty

    # 'array' is an numpy.ndarray
    if isinstance(array, numpy.ndarray):
        return array.size == 0

    # 'array' is a Sequence
    return not array


def contains_only_integers(array):
    """
    Return whether 'array' is non-empty and contains only integer values.

    Parameters
    ----------
    array: non-string Sequence or numpy.array
        array of values to evaluate

    Return value
    ------------
    bool: True if 'array' is non-empty contains only integer values;
        False otherwise

    Examples
    --------
    >>> contains_only_integers([0, 1, 2])
    True
    >>> contains_only_integers(numpy.array([0, 1, 2]))
    True
    >>> contains_only_integers(tuple([0.0, 1.0, 2.0]))
    True
    >>> contains_only_integers([0.5, 1.0, 2.0])
    False
    >>> contains_only_integers([])
    False
    """
    # --- Check arguments

    # 'array' is sequence-like but is not a string
    if not is_array(array):
        raise ValueError("'array' is not non-string Sequence or "
                         "a numpy.ndarray")

    # contents of 'array' can be converted numeric values
    try:
        _ = numpy.array(array, dtype=float)

    except Exception:
        raise ValueError("Unable to convert 'array' to an array of "
                         "numeric values")

    # Return False if 'array' is empty
    if array_is_empty(array):
        return False

    # --- Determine whether all entries of 'array' are integers

    return numpy.all(numpy.equal(numpy.mod(array, 1), 0))
