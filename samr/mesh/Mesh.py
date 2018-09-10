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
import doctest

# XYZ
from samr.mesh import MeshLevel

# --- Constants


# --- Class definition

class Mesh:
    """
    TODO
    """
    # --- Properties

    @property
    def levels(self):
        """
        list: MeshLevels in Mesh
        """
        return self._levels

    @property
    def blocks(self):
        """
        list: MeshBlocks in Mesh
        """
        num_levels = len(self.levels)
        if num_levels == 0:
            raise RuntimeError("Mesh contains no blocks.")
        elif num_levels > 1:
            raise RuntimeError("'blocks' is unavailable when for "
                               "multi-level meshes")

        return self.levels.blocks

    # --- Public methods

    def __init__(self):
        """
        TODO

        Parameters
        ----------
        TODO

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # --- Set property and attribute values

        # PYLINT: eliminate 'defined outside __init__' error
        self._levels = None


# --- Main program

if __name__ == '__main__':
    # Run doctests
    doctest.testmod()
