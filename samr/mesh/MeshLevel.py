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
from samr.geometry import Geometry

from .Box import Box
from .MeshVariable import MeshVariable
from ..utils import contains_only_integers


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

    def __init__(self, level_number, boxes, geometry):
        """
        TODO

        Parameters
        ----------
        level_number: int
            level number in Mesh

        boxes: Box or list of Boxes
            boxes that define the index space covered by MeshLevel

        geometry: Geometry
            geometry of the logically rectangular region of space (not
            necessarily coordinate space) covered by the bounding box of the
            boxes in the 'boxes' parameter

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # level_number is integer
        if not isinstance(level_number, (int, float)):
            raise ValueError("'level_number' should be a numeric value")

        # level_number is an integer value
        if level_number % 1 != 0:
            raise ValueError("'level_number' should be an integer")

        # level_number >= 0
        if level_number < 0:
            raise ValueError("'level_number' should be a non-negative number")

        # boxes
        if not isinstance(boxes, (Box, list, tuple)):
            raise ValueError("'boxes' should be a Box or a list of Boxes")

        if isinstance(boxes, (list, tuple)):
            if not boxes:
                raise ValueError("'boxes' should not be empty")

            for box in boxes:
                if not isinstance(box, Box):
                    raise ValueError("'boxes' should not contain non-Box "
                                     "items")

        else:
            # Ensure that boxes is a list
            boxes = [boxes]

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' should be a Geometry")

        # --- Initialize property and attribute values

        # level number
        self._level_number = level_number

        # blocks
        self._blocks = blocks

        # variables
        self._variables = []

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

        # 'variable' is a MeshVariable
        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' should be a MeshVariable")

        # --- Add MeshVariable to MeshLevel

        # Add 'variable' to variable list
        if variable not in self.variables:
            self._variables.append(variable)

        # Add 'variable' to all MeshBlocks
        for block in self.blocks:
            block.add_variable(variable)

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
        return "TODO"
