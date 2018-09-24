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

def contains_only_integers(array):
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
    >>> Box._contains_only_integers([0, 1, 2])
    True
    >>> Box._contains_only_integers(3)
    True
    >>> Box._contains_only_integers(numpy.array([0, 1, 2]))
    True
    >>> Box._contains_only_integers([0.0, 1.0, 2.0])
    True
    >>> Box._contains_only_integers([0.5, 1.0, 2.0])
    False
    >>> Box._contains_only_integers(3.5)
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

    # --- Determine whether all entries of 'array' are integers

    return numpy.all(numpy.equal(numpy.mod(array, 1), 0))