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
from samr.geometry import CartesianGeometry  # pylint: disable=unused-import
from samr.geometry import Geometry
from .Box import Box
from .MeshVariable import MeshVariable


# --- Class definition

class MeshBlock:
    """
    A MeshBlock object represents a logically rectangular region of space
    (i.e., a deformed rectangle). It is defined by a rectangular region of
    index space (Box object) and its mapping to a coordinate space (Geometry
    object).
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
    def variables(self):
        """
        tuple: list of MeshVariables defined on MeshBlock
        """
        return tuple(self._variables)

    @property
    def data(self):
        """
        dict: map from MeshVariables to numpy arrays containing data values
        """
        return self._data

    # --- Public methods

    def __init__(self, box, geometry):
        """
        Initialize MeshBlock object.

        Parameters
        ----------
        box: Box
            box that defines region of index space covered by MeshBlock

        geometry: Geometry
            geometry of MeshBlock

        Examples
        --------
        >>> box = Box(lower=[1, 1], upper=[10, 10])
        >>> geometry = CartesianGeometry(x_lower=[0., 0.], x_upper=[1., 1.])
        >>> block = MeshBlock(box=box, geometry=geometry)
        """
        # --- Check arguments

        # box
        if not isinstance(box, Box):
            raise ValueError("'box' is not a Box object")

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' is not a Geometry object")

        # box.num_dimensions == geometry.num_dimensions
        if box.num_dimensions != geometry.num_dimensions:
            raise ValueError("'box' and 'geometry' do not have the same "
                             "number of dimensions")

        # --- Set property and attribute values

        # box
        self._box = copy.deepcopy(box)

        # geometry
        self._geometry = copy.deepcopy(geometry)

        # variables
        self._variables = []

        # data
        self._data = {}

    def add_variable(self, variable):
        """
        Add MeshVariable to MeshBlock.

        Parameters
        ----------
        variable: MeshVariable object
            variable to add to MeshBlock

        Return value
        ------------
        None
        """
        # --- Check arguments

        # 'variable' is a MeshVariable object
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' is not a MeshVariable object")

        # --- Add MeshVariable to MeshBlock

        # Add 'variable' to variable list
        self._variables.append(variable)

        # Construct shape for data array
        # TODO: construct shape as a function of location, stencil_width, depth
        data_shape = self.shape

        # Construct data array for variable
        data = numpy.zeros(data_shape, dtype=variable.dtype)

        # Set data for variable
        self._data[id(variable)] = data

    def get_data(self, variable):
        """
        Get data array for specified variable.

        Parameters
        ----------
        variable: MeshVariable object

        Return value
        ------------
        numpy.ndarray: data array for specified variable
        """
        # --- Check arguments

        # 'variable' is a MeshVariable object
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' is not a MeshVariable object")

        # 'variable' is in data
        variable_id = id(variable)
        if variable_id not in self.data:
            error_message = \
                "'variable' (={}) not defined on MeshBlock".format(variable)
            raise ValueError(error_message)

        # --- Return data

        return self.data[variable_id]

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

        Examples
        --------
        TODO
        """
        return "MeshBlock(box={}, geometry={}, variables={})".format(
            self.box, self.geometry, self.variables)
