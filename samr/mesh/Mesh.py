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

# XYZ
from samr.box import Box
from samr.geometry import Geometry
from samr.mesh import MeshLevel
from samr.mesh import MeshVariable
from samr.utils import array_is_empty
from samr.utils import is_array
from samr.utils import is_scalar
from samr.utils import contains_only_integers


# --- Class definition

class Mesh:
    """
    A Mesh represents a collection of meshes with different levels of
    refinement (relative to the coarsest mesh level).

    TODO
    """
    # --- Properties

    @property
    def domain(self):
        """
        tuple or Box: boxes that define the index space covered by Mesh on
            the coarsest level
        """
        if len(self._domain) == 1:
            return self._domain[0]

        return tuple(self._domain)

    @property
    def bounding_box(self):
        """
        Box: smallest Box on coarsest level of Mesh that covers domain
        """
        return self._bounding_box

    @property
    def geometry(self):
        """
        Geometry: geometry of bounding box of domain
        """
        return self._geometry

    @property
    def num_dimensions(self):
        """
        int: dimensionality of index space
        """
        return self.geometry.num_dimensions

    @property
    def levels(self):
        """
        tuple: MeshLevels in Mesh
        """
        return tuple(self._levels)

    @property
    def num_levels(self):
        """
        int: number of MeshLevels in Mesh
        """
        return len(self.levels)

    @property
    def blocks(self):
        """
        tuple: MeshBlocks in Mesh

        Notes
        -----
        * Only available when Mesh.is_single_level is True (i.e., Mesh is
          created with single_level=True)
        """
        if not self.is_single_level:
            raise RuntimeError("Mesh is multi-level. "
                               "'blocks' is unavailable")

        return self.levels[0].blocks

    @property
    def num_blocks(self):
        """
        int: number of MeshBlocks in Mesh

        Notes
        -----
        * Only available when Mesh.is_single_level is True (i.e., Mesh is
          created with single_level=True)
        """
        if not self.is_single_level:
            raise RuntimeError("Mesh is multi-level. "
                               "'num_blocks' is unavailable")

        return self.levels[0].num_blocks

    @property
    def block(self):
        """
        MeshBlock: MeshBlock in Mesh

        Notes
        -----
        * Only available when Mesh.is_single_block is True (i.e., Mesh is
          created with a single-box domain and single_level=True)
        """
        if not self.is_single_block:
            raise RuntimeError("Mesh is not single-block. "
                               "'block' is unavailable")

        return self.levels[0].blocks[0]

    @property
    def variables(self):
        """
        tuple: list of MeshVariables defined on Mesh
        """
        return tuple(self._variables)

    @property
    def is_single_level(self):
        """
        boolean: True if Mesh contains only one MeshLevel; False otherwise
        """
        return self.num_levels == 1

    @property
    def is_single_block(self):
        """
        boolean: True if Mesh is single-level and domain contains only one
            Box; False otherwise
        """
        return self.is_single_level and len(self._domain) == 1

    # --- Public methods

    def __init__(self, domain, first_box_geometry):
        """
        Initialize Mesh.

        Parameters
        ----------
        domain: Box or list of Boxes
            boxes that define the index space covered by Mesh on the coarsest
            level

        first_box_geometry: Geometry
            geometry of the logically rectangular region of space (not
            necessarily coordinate space) covered by the first box in the
            'domain' parameter

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # check domain parameter
        if isinstance(domain, Box):

            # ensure that domain is a list
            domain = [domain]

        elif is_array(domain, exclude_numpy_ndarray=True):

            # domain is not empty
            if not domain:
                raise ValueError("'domain' should not be empty")

            # domain contains only Box items
            for box in domain:
                if not isinstance(box, Box):
                    raise ValueError("'domain' should not contain non-Box "
                                     "items")

        else:
            # domain does not have a valid type
            raise ValueError("'domain' should be a Box or a list of Boxes")

        # first_box_geometry has expected type
        if not isinstance(first_box_geometry, Geometry):
            raise ValueError("'first_box_geometry' should be a Geometry")

        # --- Initialize property and attribute values

        # index space
        self._domain = copy.deepcopy(domain)
        self._bounding_box = Box.compute_bounding_box(self.domain)

        # geometry
        self._geometry = first_box_geometry.compute_geometry(
            domain[0], self.bounding_box)

        # refinement levels
        self._levels = []

        # variables
        self._variables = []

        # --- Initialize coarsest MeshLevel

        self.add_level(domain, first_box_geometry)

    def create_variable(self,
                        location=None, max_stencil_width=None,
                        depth=None, precision=None,
                        level_numbers=None):
        """
        Create MeshVariable on specified levels.

        Parameters
        ----------
        location: Location
            location of MeshVariable values in mesh cell

        max_stencil_width: int or list of ints
            maximum width of stencil applied to MeshVariable

        depth: int
            number of components of MeshVariable

        precision: Precision
            floating-point precision for MeshVariable

        level_numbers: int or list of ints
            level numbers that variable should be added to

        Return value
        ------------
        MeshVariable: newly created MeshVariable
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-branches

        # --- Check arguments

        # check level_numbers parameter
        if level_numbers is not None:

            # level_numbers is not empty
            if is_array(level_numbers):
                if array_is_empty(level_numbers):
                    raise ValueError("'level_numbers' should not be empty")

            elif is_scalar(level_numbers):

                # ensure that level_numbers is a list
                level_numbers = [level_numbers]

            else:
                # level_numbers does not have a valid type
                raise ValueError("'level_numbers' should be a scalar, a "
                                 "list-like collection of integers, or a "
                                 "numpy.ndarray")

            # level_numbers contains only integers
            if not contains_only_integers(level_numbers):
                raise ValueError("'level_numbers' should contain only integer "
                                 "values")

            # min(level_numbers) >= 0
            if min(level_numbers) < 0:
                raise ValueError("'level_numbers' should not contain negative "
                                 "values")

            # max(level_numbers) < mesh.num_levels
            if max(level_numbers) >= self.num_levels:
                raise ValueError("'level_numbers' should only contain values "
                                 "less than number of levels in the Mesh")

        # MeshVariable parameters are checked by MeshVariable.__init__():
        #   - location
        #   - max_stencil_width
        #   - depth
        #   - precision

        # --- Create new MeshVariable and add it to Mesh

        # Construct variable parameter dict
        variable_parameters = {}
        if location is not None:
            variable_parameters['location'] = location
        if max_stencil_width is not None:
            variable_parameters['max_stencil_width'] = max_stencil_width
        if depth is not None:
            variable_parameters['depth'] = depth
        if precision is not None:
            variable_parameters['precision'] = precision

        # Create MeshVariable
        variable = MeshVariable(self, **variable_parameters)

        # Add variable to Mesh
        self._variables.append(variable)

        # Convert level numbers to levels
        if level_numbers is None:
            levels = self.levels
        else:
            levels = [self.levels[level_num] for level_num in level_numbers]

        # Add variable to levels
        for level in levels:
            level.add_variable(variable)

        # --- Return MeshVariable

        return variable

    def add_level(self, boxes, first_box_geometry):
        """
        Add new MeshLevel to Mesh with level number set to 'num_levels'.

        Parameters
        ----------
        boxes: Box or list of Boxes
            boxes that define the index space covered by MeshLevel

        first_box_geometry: Geometry
            geometry of the logically rectangular region of space (not
            necessarily coordinate space) covered by the first box in the
            'boxes' parameter

        Return value
        ------------
        None

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # MeshLevel parameters are checked by MeshLevel.__init__():
        #   - boxes
        #   - first_box_geometry

        # --- Create and set up new MeshLevel

        # Create MeshLevel
        level = MeshLevel(self.num_levels, boxes, first_box_geometry)

        # Add new MeshLevel to Mesh
        self._levels.append(level)

        # Add existing variables to new MeshLevel
        for variable in self.variables:
            level.add_variable(variable)

    def remove_level(self):
        """
        Remove MeshLevel at the highest level of refinement from Mesh.

        Parameters
        ----------
        None

        Return value
        ------------
        MeshLevel: MeshLevel removed from Mesh

        Notes
        -----
        * It is an error to attempt to remove the coarsest MeshLevel in the
          Mesh.

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # Mesh contains at least two levels
        if self.num_levels == 1:
            raise RuntimeError("The coarsest MeshLevel cannot be removed "
                               "from Mesh")

        # --- Remove and return MeshLevel at highest level of refinement

        level = self.levels[-1]
        del self._levels[-1]

        return level

    def data(self, variable):
        """
        Retrieve data array for specified variable.

        Parameters
        ----------
        variable: MeshVariable
            variable to retrieve data array for

        Return value
        ------------
        numpy.ndarray: data array for specified variable

        Notes
        -----
        * Only available when Mesh.is_single_block is True (i.e., Mesh is
          created with a single-box domain and single_level=True)
        """
        # --- Check arguments

        # Mesh is single-block
        if not self.is_single_block:
            raise RuntimeError("Mesh is not single-block. "
                               "'data' is unavailable")

        # variable has expected type
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' should be a MeshVariable")

        # variable is in variable list for Mesh
        if variable not in self.variables:
            raise ValueError("'variable' is not in the variable list for Mesh")

        # --- Retrieve data array

        return variable.data(self.levels[0].blocks[0])

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
        return "Mesh(domain={}, levels={}, variables={}, " \
               "single_level={}, single_block={})". \
               format(list(self.domain), list(self.levels),
                      list(self.variables),
                      self.is_single_level, self.is_single_block)
