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

# XYZ
# TODO

# --- Constants


# --- Class definition

class MeshBlock:
    """
    TODO
    """
    # --- Properties

    @property
    def geometry(self):
        """
        BlockGeometry: geometry of MeshBlock
        """
        return self._geometry

    @property
    def data(self):
        """
        dict: mapping from MeshVariables to numpy arrays containing
              data values
        """
        return self._data

    # --- Public methods

    def __init__(self, geometry):
        """
        TODO

        Parameters
        ----------
        geometry: BlockGeometry
            TODO

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # --- Set property and attribute values

        # PYLINT: eliminate 'defined outside __init__' error
        self._data = {}

        self._geometry = geometry

    def add_variable(self, mesh_variable):
        """
        TODO
        """
        # Construct data array for variable
        data = numpy.array(1)

        # Set data for variable
        self._data[mesh_variable] = data

    def get_data(self, mesh_variable):
        """
        TODO
        """
        # --- Check arguments

        if mesh_variable not in self.data:
            err_msg = "'mesh_variable' (={}) not defined on MeshBlock". \
                format(mesh_variable)
            raise ValueError(err_msg)

        # --- Return data

        return self.data[mesh_variable]
