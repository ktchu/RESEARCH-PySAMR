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
from samr.geometry import Geometry

from .Box import Box
from .MeshBlock import MeshBlock
from .MeshLevel import MeshLevel
from .MeshVariable import MeshVariable

from .utils import array_is_empty
from .utils import contains_only_integers


# --- Class definition

class Mesh:
    """
    A Mesh object represents a collection of meshes with different levels of
    refinement (relative to the coarsest mesh level).

    TODO
    """
    # --- Properties

    @property
    def domain(self):
        """
        list: boxes that define the index space covered by Mesh on the
              coarsest level
        """
        return self._domain

    @property
    def bounding_box(self):
        """
        Box: smallest Box on coarsest level of mesh that covers domain
        """
        return self._bounding_box

    @property
    def geometry(self):
        """
        Geometry: geometry for Mesh on the coarsest level
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
        boolean: True if Mesh is single-level; False otherwise
        """
        return self._is_single_level

    @property
    def is_single_block(self):
        """
        boolean: True if Mesh is single-block; False otherwise
        """
        return self._is_single_block

    # --- Public methods

    def __init__(self, domain, geometry, single_level=False):
        """
        Initialize Mesh object.

        Parameters
        ----------
        domain: Box or list of Boxes
            boxes that define the index space covered by Mesh on the coarsest
            level

        geometry: Geometry
            geometry for Mesh on the coarsest level. Geometry parameters
            provided by 'geometry' apply to the bounding box for 'domain'.

        single_level: boolean
            True if Mesh will contain at most one level; False otherwise

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # domain
        if not isinstance(domain, (Box, list, tuple)):
            raise ValueError("'domain' is not a Box object or a list of "
                             "Box objects")

        if isinstance(domain, (list, tuple)):
            if not domain:
                raise ValueError("'domain' is empty")

            for box in domain:
                if not isinstance(box, Box):
                    raise ValueError("'domain' contains a non-Box object")

        else:
            # Ensure that domain is a list
            domain = [domain]

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' is not a Geometry object")

        # --- Initialize property and attribute values

        # index space
        self._domain = copy.deepcopy(domain)
        self._bounding_box = Box.compute_bounding_box(self.domain)

        # geometry
        self._geometry = copy.deepcopy(geometry)

        # refinement levels
        self._levels = []

        # variables
        self._variables = []

        # mesh type
        self._is_single_level = single_level

        if self.is_single_level:
            self._is_single_block = len(self._domain) == 1
        else:
            self._is_single_block = False

        # --- Initialize coarsest MeshLevel

        blocks = []
        for box in domain:
            # TODO: fix computation of geometry for block
            block_geometry = self.geometry
            blocks.append(MeshBlock(box, block_geometry))

        level = MeshLevel(level_number=0, blocks=blocks)
        self._levels.append(level)

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
        variable: MeshVariable object
            newly created MeshVariable object
        """
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-branches

        # --- Check arguments

        # level_numbers
        if level_numbers is not None:
            if not isinstance(level_numbers, (int, float, list, tuple)):
                raise ValueError("'level_numbers' is not a scalar or a list "
                                 "of integers")

            # level_numbers is not empty
            if isinstance(level_numbers, (list, tuple)):
                if array_is_empty(level_numbers):
                    raise ValueError("'level_numbers' is empty")
            else:
                # Ensure that level_numbers is a list
                level_numbers = [level_numbers]

            # level_numbers contains only integers
            if not contains_only_integers(level_numbers):
                raise ValueError("'level_numbers' contains non-integer values")

            # min(level_numbers) >= 0
            if min(level_numbers) < 0:
                raise ValueError("'level_numbers' contains negative values")

            # max(level_numbers) < mesh.num_levels
            if max(level_numbers) >= self.num_levels:
                raise ValueError("'level_numbers' contains values larger "
                                 "maximum level number in mesh")

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

    def add_level(self, blocks):
        """
        Add a MeshLevel to Mesh.

        Parameters
        ----------
        blocks: MeshBlock object or list of MeshBlock objects
            blocks that make up new refinement level

        Return value
        ------------
        None

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # let MeshLevel.__init__() check 'blocks'

        # --- Create and set up new MeshLevel

        level = MeshLevel(self.num_levels, blocks)
        for variable in self.variables:
            level.add_variable(variable)

        self._levels.append(level)

    def data(self, variable):
        """
        Retrieve data array for specified variable.

        Parameters
        ----------
        variable: MeshVariable object
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

        # 'variable' is a MeshVariable object
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' is not a MeshVariable object")

        # 'variable' is not in variable list for Mesh
        if variable not in self.variables:
            raise ValueError("'variable' is in variable list for Mesh")

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
        return "Mesh(domain={}, geometry={}, variables={}, " \
               "single_level={}, single_block={})". \
               format(self.domain, self.geometry, self.variables,
                      self.is_single_level, self.is_single_block)
