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
from samr.mesh import MeshBlock

# --- Constants


# --- Class definition

class MeshLevel:
    """
    TODO
    """
    # --- Properties

    @property
    def blocks(self):
        """
        list: MeshBlocks in Mesh
        """
        return self._blocks

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
        self._blocks = None
