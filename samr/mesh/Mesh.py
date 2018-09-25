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
    def blocks(self, level_number=0):
        """
        tuple: MeshBlocks in Mesh
        """
        if level_number > self.num_levels:
            raise RuntimeError("'level_number' exceeds the number of levels "
                               "in Mesh")

        return self.levels[level_number].blocks

    @property
    def num_blocks(self, level_number=0):
        """
        int: number of MeshBlocks in Mesh
        """
        if level_number > self.num_levels:
            raise RuntimeError("'level_number' exceeds the number of levels "
                               "in Mesh")

        return len(self.blocks)

    @property
    def variables(self):
        """
        tuple: list of MeshVariables defined on Mesh
        """
        return tuple(self._variables)

    @property
    def data(self, variable, block_number=0):
        """
        TODO
        """
        # TODO
        pass

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

    def __init__(self, domain, geometry,
                 single_level=False, single_block=False):
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

        single_block: boolean
            True if Mesh will contain at most one block; False otherwise

        Notes
        -----
        * When 'single_block' is set to True, the Mesh.is_single_level is
          set to True. The value of the 'single_level' parameter is ignored.

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

        # --- Set property and attribute values

        # index space
        self._domain = copy.deepcopy(domain)
        self._bounding_box = Box.compute_bounding_box(self.domain)

        # geometry
        self._geometry = copy.deepcopy(geometry)

        # refinement levels
        self._levels = []

        # variables
        self._variables = []

        # is_single_block
        self._is_single_block = single_block

        # is_single_level
        if self.is_single_block:
            self._is_single_level = True
        else:
            self._is_single_level = single_level

        # --- Initialize levels for single-level meshes

        if single_block:
            block = MeshBlock(self.domain[0], self.geometry)
            level = MeshLevel(level_number=0, blocks=[block])
            self._levels.append(level)

        else:
            blocks = []
            for box in domain:
                # TODO: fix computation of geometry for block
                block_geometry = self.geometry
                blocks.append(MeshBlock(box, block_geometry))

            level = MeshLevel(level_number=0, blocks=blocks)
            self._levels.append(level)

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

    def create_variable(self, level_numbers=None):
        """
        Create MeshVariable on specified levels.

        Parameters
        ----------
        level_numbers: int or list of ints
            level numbers that variable should be added to

        TODO: other parameters

        Return value
        ------------
        variable: MeshVariable object
            newly created MeshVariable object
        """
        # TODO: add parameters for MeshVariable

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

        # --- Create MeshVariable and add it to Mesh

        # Create MeshVariable
        # TODO: add variable parameters
        variable = MeshVariable(self)

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
        return "Mesh(domain={}, geometry={}, variables={}, " \
               "single_level={}, single_block={})". \
               format(self.domain, self.geometry, self.variables,
                      self.is_single_level, self.is_single_block)
