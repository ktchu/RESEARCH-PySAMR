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
from samr.geometry import Geometry
from samr.mesh import Box


# --- Class definition

class MeshBlock:
    """
    TODO
    """
    # --- Properties

    @property
    def box(self):
        """
        int: dimensionality of index space
        """
        return self._box

    @property
    def geometry(self):
        """
        Geometry: geometry of MeshBlock
        """
        return self._geometry

    @property
    def lower(self):
        """
        numpy.ndarray: lower corner of index space covered by MeshBlock
        """
        return self.box.lower

    @property
    def upper(self):
        """
        numpy.ndarray: upper corner of index space covered by MeshBlock
        """
        return self.box.upper

    @property
    def num_dimensions(self):
        """
        int: dimensionality of index space
        """
        return self.box.num_dimensions

    @property
    def shape(self):
        """
        tuple: number of cells in each coordinate direction
        """
        return self.box.shape

    @property
    def size(self):
        """
        int: number of cells in MeshBlock
        """
        return self.box.size

    @property
    def data(self):
        """
        dict: mapping from MeshVariables to numpy arrays containing
              data values
        """
        return self._data

    # --- Public methods

    def __init__(self, box, geometry):
        """
        Initialize MeshBlock.

        Parameters
        ----------
        box: Box
            box that defines region of index space covered by MeshBlock

        geometry: Geometry
            geometry of MeshBlock

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # box
        if not isinstance(box, Box):
            raise ValueError("'box' is not Box object")

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' is not Geometry object")

        # box.num_dimensions == geometry.num_dimensions
        if box.num_dimensions != geometry.num_dimensions:
            error_message = "'box' and 'geometry' do not have the same " \
                            "number of dimensions"
            raise ValueError(error_message)

        # --- Set property and attribute values

        # PYLINT: eliminate 'defined outside __init__' error
        self._data = {}

        # box
        self._box = box

        # geometry
        self._geometry = geometry

        # index space
        # self._lower = lower.astype('int64')
        # self._upper = upper.astype('int64')

    def add_variable(self, variable):
        """
        Add MeshVariable to MeshBlock.

        Parameters
        ----------
        variable: MeshVariable
            MeshVariable to add to MeshBlock

        Return value
        ------------
        None
        """
        # Construct data array for variable
        data = numpy.array(self.shape, dtype=variable.dtype)

        # Set data for variable
        self._data[variable] = data

    def get_data(self, variable):
        """
        TODO
        """
        # --- Check arguments

        if variable not in self.data:
            error_message = "'variable' (={}) not defined on MeshBlock". \
                format(variable)
            raise ValueError(error_message)

        # --- Return data

        return self.data[variable]
