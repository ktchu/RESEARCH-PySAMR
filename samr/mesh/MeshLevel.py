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

# XYZ
from samr.box import Box
from samr.geometry import CartesianGeometry  # pylint: disable=unused-import
from samr.geometry import Geometry

from .MeshBlock import MeshBlock
from .MeshVariable import MeshVariable

from ..utils import is_array
from ..utils import is_scalar


# --- Constants


# --- Class definition

class MeshLevel:
    """
    A MeshLevel represents a region of space is defined as the union of a
    collection of logically rectangular regions with the same level of
    refinement (relative to the coarsest level in Mesh).
    """
    # --- Properties

    @property
    def level_number(self):
        """
        int: level number in Mesh
        """
        return self._level_number

    @property
    def blocks(self):
        """
        tuple: MeshBlocks in MeshLevel
        """
        return tuple(self._blocks)

    @property
    def num_blocks(self):
        """
        int: number of MeshBlocks in MeshLevel
        """
        return len(self._blocks)

    @property
    def variables(self):
        """
        tuple: list of MeshVariables defined on MeshLevel
        """
        return tuple(self._variables)

    # --- Public methods

    def __init__(self, level_number, boxes, first_box_geometry):
        """
        Initialize MeshLevel.

        Parameters
        ----------
        level_number: int
            level number in Mesh

        boxes: Box or list of Boxes
            boxes that define the index space covered by MeshLevel

        first_box_geometry: Geometry
            geometry of the logically rectangular region of space (not
            necessarily coordinate space) covered by the first box in the
            'boxes' parameter

        Examples
        --------
        >>> level_number = 1
        >>> boxes = [Box([0, 0], [9, 9]), Box([0, 10], [9, 19])]
        >>> first_box_geometry = CartesianGeometry([0, 0], [1, 1])
        >>> level = MeshLevel(level_number, boxes, first_box_geometry)
        """
        # --- Check arguments

        # level_number is integer
        if not is_scalar(level_number):
            raise ValueError("'level_number' should be a numeric value")

        # level_number is an integer value
        if level_number % 1 != 0:
            raise ValueError("'level_number' should be an integer")

        # level_number >= 0
        if level_number < 0:
            raise ValueError("'level_number' should be a non-negative number")

        # boxes
        #
        # Note: _generate_blocks() performs additional check on boxes
        if isinstance(boxes, Box):
            # Ensure that boxes is a list
            boxes = [boxes]

        elif not is_array(boxes, exclude_numpy_ndarray=True):
            raise ValueError("'boxes' should be a Box or a list of Boxes")

        # first_box_geometry
        if not isinstance(first_box_geometry, Geometry):
            raise ValueError("'first_box_geometry' should be a Geometry")

        # --- Initialize property and attribute values

        # level number
        self._level_number = level_number

        # variables
        self._variables = []

        # blocks
        self._blocks = MeshLevel._generate_blocks(boxes, first_box_geometry)

    def add_variable(self, variable):
        """
        Add MeshVariable to MeshLevel.

        Parameters
        ----------
        variable: MeshVariable
            variable to add to MeshLevel

        Return value
        ------------
        None
        """
        # --- Check arguments

        # variable is a MeshVariable
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' should be a MeshVariable")

        # --- Add MeshVariable to MeshLevel

        # Add variable to self.variables
        if variable not in self.variables:
            self._variables.append(variable)

        # Add variable to all MeshBlocks
        for block in self.blocks:
            block.add_variable(variable)

    # --- Private helper methods

    @staticmethod
    def _generate_blocks(boxes, first_box_geometry):
        """
        Generate MeshBlocks for MeshLevel.

        Parameters
        ----------
        boxes: list of Boxes
            boxes that define the index spaces of the MeshBlocks to generate

        first_box_geometry: Geometry
            geometry of the logically rectangular region of space (not
            necessarily coordinate space) covered by the first box in the
            'boxes' parameter

        Return value
        ------------
        list of MeshBlocks
        """
        # --- Check arguments

        # boxes is list-like
        if not is_array(boxes, exclude_numpy_ndarray=True):
            raise ValueError("'boxes' should be a list of Boxes")

        # boxes is not empty
        if not boxes:
            raise ValueError("'boxes' should not be empty")

        # boxes contains only Boxes
        for box in boxes:
            if not isinstance(box, Box):
                raise ValueError("'boxes' should not contain non-Box items")

        # first_box_geometry
        if not isinstance(first_box_geometry, Geometry):
            raise ValueError("'first_box_geometry' should be a Geometry")

        # --- Generate blocks

        blocks = [MeshBlock(boxes[0], first_box_geometry)]
        for box in boxes[1:]:
            geometry = first_box_geometry.compute_geometry(boxes[0], box)
            blocks.append(MeshBlock(box, geometry))

        return blocks

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
        return "MeshLevel(level_number={}, blocks={}, variables={})". \
               format(self.level_number, list(self.blocks),
                      list(self.variables))
