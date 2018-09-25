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
from .MeshBlock import MeshBlock
from .MeshVariable import MeshVariable


# --- Constants


# --- Class definition

class MeshLevel:
    """
    A MeshLevel object represents a region of space is defined as the union
    of a collection of logically rectangular regions with the same level of
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

    def __init__(self, level_number, blocks):
        """
        TODO

        Parameters
        ----------
        level_number: int
            level number in Mesh

        blocks: MeshBlock object or list of MeshBlock objects
            MeshBlocks in MeshLevel

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # level_number is integer
        # TODO

        # level_number >= 0
        # TODO

        # blocks
        if not isinstance(blocks, (MeshBlock, list, tuple)):
            raise ValueError("'blocks' is not a MeshBlock object or a list "
                             "of MeshBlock objects")

        if isinstance(blocks, (list, tuple)):
            for block in blocks:
                if not isinstance(block, MeshBlock):
                    raise ValueError("'blocks' contains a non-MeshBlock "
                                     "object")
        else:
            # Ensure that blocks is a list
            blocks = [blocks]

        # --- Set property and attribute values

        self._level_number = level_number
        self._blocks = blocks
        self._variables = []

    def add_variable(self, variable):
        """
        Add MeshVariable to MeshLevel.

        Parameters
        ----------
        variable: MeshVariable object
            variable to add to MeshLevel

        Return value
        ------------
        None
        """
        # --- Check arguments

        if not isinstance(variable, MeshVariable):
            raise ValueError("'variable' is not a MeshVariable object")

        # --- Add MeshVariable to MeshLevel

        # Add 'variable' to variable list
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
