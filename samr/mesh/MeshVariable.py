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
from samr.mesh import Mesh

# --- Constants


# --- Class definition

class MeshVariable:
    """
    TODO
    """
    # --- Properties

    @property
    def mesh(self):
        """
        Mesh: mesh that MeshVariable is defined on
        """
        return self._mesh

    @property
    def dtype(self):
        """
        numpy.dtype: data type of MeshVariable
        """
        return self._dtype

    # --- Public methods

    def __init__(self, mesh, precision='double'):
        """
        Initialize MeshVariable object.

        Parameters
        ----------
        mesh: Mesh object
            mesh that MeshVariable is defined on

        precision: str
            floating-point precision for MeshVariable.
            Valid values: 'double', 'single'.

        Examples
        --------
        TODO
        """
        # --- Check arguments

        if not isinstance(mesh, Mesh):
            raise ValueError("'mesh' is not a Mesh object")

        if precision not in ['double', 'single']:
            raise ValueError("'precision' does not equal 'double' or 'single'")

        # --- Set property and attribute values

        self._mesh = mesh

        if precision == 'double':
            self._dtype = numpy.float64
        else:
            self._dtype = numpy.float32
