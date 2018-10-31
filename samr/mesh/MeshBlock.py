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
import copy

# External packages
import numpy

# XYZ
from samr.box import Box
from samr.geometry import CartesianGeometry  # pylint: disable=unused-import
from samr.geometry import Geometry

from .MeshVariable import MeshVariable


# --- Class definition

class MeshBlock:
    """
    A MeshBlock represents a logically rectangular region of space (i.e., a
    deformed rectangle). It is defined by a rectangular region of index space
    (Box) and its mapping to a coordinate space (Geometry). It manages array
    data for MeshVariables defined on the region of space.
    """
    # --- Properties

    @property
    def box(self):
        """
        Box: index space of MeshBlock
        """
        return self._box

    @property
    def geometry(self):
        """
        Geometry: geometry of MeshBlock
        """
        return self._geometry

    @property
    def num_dimensions(self):
        """
        int: dimensionality of index space
        """
        return self.box.num_dimensions

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
    def shape(self):
        """
        numpy.ndarray: number of cells in each coordinate direction
        """
        return self.box.shape

    @property
    def size(self):
        """
        int: number of cells in MeshBlock
        """
        return self.box.size

    @property
    def stores_vectors_contiguously(self):
        """
        bool: True if components of vector-valued MeshVariables are stored
              contiguously in memory; False if each component of vector-valued
              MeshVariables is individually stored as a slice in memory.
        """
        return self._stores_vectors_contiguously

    @property
    def variables(self):
        """
        tuple: list of MeshVariables defined on MeshBlock
        """
        return tuple(self._variables)

    # --- Public methods

    def __init__(self, box, geometry,
                 stores_vectors_contiguously=True):
        """
        Initialize MeshBlock.

        Parameters
        ----------
        box: Box
            box that defines region of index space covered by MeshBlock

        geometry: Geometry
            geometry of MeshBlock

        stores_vectors_contiguously: bool
            When set to True, store components of vector-valued MeshVariable
            (i.e., depth > 1) contiguously in memory. When set to False, store
            component of vector-valued MeshVariable as slices in memory (i.e.,
            each component of MeshVariable is individually stored contiguously
            in memory).

        Examples
        --------
        >>> box = Box(lower=[1, 1], upper=[10, 10])
        >>> geometry = CartesianGeometry(x_lower=[0., 0.], x_upper=[1., 1.])
        >>> block = MeshBlock(box=box, geometry=geometry)
        """
        # --- Check arguments

        # box has expected type
        if not isinstance(box, Box):
            raise ValueError("'box' should be a Box")

        # geometry has expected type
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' should be a Geometry")

        # box.num_dimensions == geometry.num_dimensions
        if box.num_dimensions != geometry.num_dimensions:
            raise ValueError("'box' and 'geometry' should have the same "
                             "number of dimensions")

        # --- Initialize property and attribute values

        # box
        self._box = copy.deepcopy(box)

        # geometry
        self._geometry = copy.deepcopy(geometry)

        # variables
        self._variables = []

        # data storage properties
        self._stores_vectors_contiguously = stores_vectors_contiguously

        # data
        self._data = {}

    def add_variable(self, variable):
        """
        Add MeshVariable to MeshBlock.

        Parameters
        ----------
        variable: MeshVariable
            variable to add to MeshBlock

        Return value
        ------------
        None
        """
        # --- Check arguments

        # variable has expected type
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' should be a MeshVariable")

        # Exit if variable has already been added to MeshBlock
        if variable in self.variables:
            return

        # --- Add MeshVariable to MeshBlock

        # Add 'variable' to variable list
        self._variables.append(variable)

        # Construct data arrays for variable
        self._data[id(variable)] = self._create_data(variable)

    def data(self, variable=None):
        """
        Get data array for a specified variable.

        Parameters
        ----------
        variable: MeshVariable

        Return value
        ------------
        numpy.ndarray or dict:
            When 'variable' is set, return data array for specified variable.
            When 'variable' is not set, return map from MeshVariables to
            numpy arrays containing data values.
        """
        # --- Return self._data when 'variable' is not set

        if variable is None:
            return self._data

        # --- Check arguments

        # variable has expected type
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' should be a MeshVariable")

        # variable is in self.data
        variable_id = id(variable)
        if variable_id not in self._data:
            error_message = "'variable' (={}) is not defined on MeshBlock". \
                format(variable)
            raise ValueError(error_message)

        # --- Return data

        return self._data[variable_id]

    # --- Private helper methods

    def _create_data(self, variable):
        """
        Create array data for MeshVariable.

        Parameters
        ----------
        variable: MeshVariable
            variable to create array data for

        Return value
        ------------
        numpy.ndarray or list:
            array data for MeshVariable on 'block'

        Notes
        -----
        * When the depth of the MeshVariable is 1, the return value is an
          numpy.ndarray. When the depth of the MeshVariable is greater than
          1, the return value is a list of numpy.ndarray objects.
        """
        # pylint: disable=too-many-branches

        # --- Check arguments

        # 'variable' has expected type
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' should be a MeshVariable")

        # 'variable' is in variable list
        if variable not in self.variables:
            raise ValueError("'variable' should be in variable list for "
                             "MeshBlock")

        # --- Initialize data

        data = None

        # --- Create numpy.ndarrays for data

        # Compute shape of box for MeshVariable with halo on 'block'
        box_shape = variable.box(self, with_halo=True).shape

        if variable.location in \
                [MeshVariable.Location.CELL, MeshVariable.Location.NODE]:

            # --- Case: self.location is CELL or NODE

            # Compute shape of data
            if variable.location is MeshVariable.Location.CELL:
                data_shape = box_shape

            elif variable.location is MeshVariable.Location.NODE:
                data_shape = box_shape + 1

            # Add dimension for vector-valued MeshVariables
            if variable.depth > 1:
                if self.stores_vectors_contiguously:
                    data_shape = \
                        numpy.array(list(data_shape) + [variable.depth])
                else:
                    data_shape = \
                        numpy.array([variable.depth] + list(data_shape))

            # Create data array
            data = numpy.zeros(data_shape, dtype=variable.dtype)

        elif variable.location == MeshVariable.Location.FACE:

            # --- Case: MeshVariable values location is FACE

            # Initialize data to be an empty list
            data = []

            # Loop over coordinate directions to construct data array
            for i in range(self.num_dimensions):
                # Compute shape of data
                data_shape = copy.deepcopy(box_shape)
                data_shape[i] += 1

                # Add dimension for vector-valued MeshVariables
                if variable.depth > 1:
                    if self.stores_vectors_contiguously:
                        data_shape = \
                            numpy.array(list(data_shape) + [variable.depth])
                    else:
                        data_shape = \
                            numpy.array([variable.depth] + list(data_shape))

                # Create data array
                data.append(numpy.zeros(data_shape, dtype=variable.dtype))

        # --- Return newly created data objects

        return data

    # --- Magic methods

    def __repr__(self):
        """
        Return unambiguous representation of object.

        Parameters
        ----------
        None

        Return value
        ------------
        str: unambiguous string representation of object
        """
        return "MeshBlock(box={}, geometry={}, variables={})".format(
            self.box, self.geometry, list(self.variables))
