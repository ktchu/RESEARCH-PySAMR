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
import doctest

# External packages
import numpy

# --- Constants


# --- Class definition

class MeshVariable:
    """
    TODO
    """
    # --- Properties

    @property
    def dtype(self):
        """
        numpy.dtype: data type of MeshVariable
        """
        return self._dtype

    # --- Public methods

    def __init__(self, precision='double'):
        """
        Initialize MeshVariable object.

        Parameters
        ----------
        precision: str
            floating-point precision for MeshVariable.
            Valid values: 'double', 'single'.

        Examples
        --------
        TODO
        """
        # --- Check arguments

        if precision not in ['double', 'single']:
            raise ValueError("'precision' must be set to 'double' or 'single'")

        # --- Set property and attribute values

        if precision == 'double':
            self._dtype = numpy.float64
        else:
            self._dtype = numpy.float32


# --- Main program

if __name__ == '__main__':
    # Run doctests
    doctest.testmod()
