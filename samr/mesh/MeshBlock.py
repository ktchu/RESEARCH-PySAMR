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
# TODO
from samr.geometry import Geometry


# --- Constants

# numpy integer data types
from .constants import NUMPY_INT_DTYPES


# --- Class definition

class MeshBlock:
    """
    TODO
    """
    # --- Properties

    @property
    def num_dimensions(self):
        """
        int: dimensionality of index space
        """
        return self._geometry.num_dimensions

    @property
    def lower(self):
        """
        numpy.ndarray: lower corner of index space covered by MeshBlock

        Notes
        -----
        * lower.dtype = 'int64'
        """
        return self._lower

    @property
    def upper(self):
        """
        numpy.ndarray: upper corner of index space covered by MeshBlock

        Notes
        -----
        * upper.dtype = 'int64'
        """
        return self._upper

    @property
    def shape(self):
        """
        tuple: number of cells in each coordinate direction
        """
        return self.upper - self.lower + numpy.ones(self.num_dimensions)

    @property
    def geometry(self):
        """
        Geometry: geometry of MeshBlock
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

    def __init__(self, geometry, lower, upper):
        """
        Initialize MeshBlock.

        Parameters
        ----------
        geometry: Geometry
            geometry of MeshBlock

        lower: numpy.ndarray of integers
            lower corner of index space covered by MeshBlock

        upper: numpy.ndarray of integers
            upper corner of index space covered by MeshBlock

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' is not Geometry object")

        # get dimensionality of geometry
        num_dimensions = geometry.num_dimensions

        # lower
        if not isinstance(lower, numpy.ndarray):
            raise ValueError("'lower' is not a numpy.ndarray")

        if len(lower) != num_dimensions:
            err_msg = "'lower' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        if lower.dtype not in NUMPY_INT_DTYPES:
            err_msg = "'lower' does not have an integer dtype"
            raise ValueError(err_msg)

        # upper
        if not isinstance(upper, numpy.ndarray):
            raise ValueError("'upper' is not a numpy.ndarray")

        if len(upper) != num_dimensions:
            err_msg = "'upper' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        if upper.dtype not in NUMPY_INT_DTYPES:
            err_msg = "'upper' does not have an integer dtype"
            raise ValueError(err_msg)

        # upper > lower
        if not numpy.all(numpy.greater(upper, lower)):
            err_msg = "Some components of 'upper' are less than or equal " \
                      "to components of 'lower'"
            raise ValueError(err_msg)

        # --- Set property and attribute values

        # PYLINT: eliminate 'defined outside __init__' error
        self._data = {}

        # index space
        self._lower = lower.astype('int64')
        self._upper = upper.astype('int64')

        # geometry
        self._geometry = geometry

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
