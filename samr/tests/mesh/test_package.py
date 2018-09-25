"""
Unit tests for 'mesh' package.

------------------------------------------------------------------------------
COPYRIGHT/LICENSE.  This file is part of the XYZ package.  It is subject
to the license terms in the LICENSE file found in the top-level directory of
this distribution.  No part of the XYZ package, including this file, may be
copied, modified, propagated, or distributed except according to the terms
contained in the LICENSE file.
------------------------------------------------------------------------------
"""
# --- Imports

# XYZ
from samr import mesh


# --- Tests

def test_attributes():
    """
   Test for expected package attributes.
    """
    # Package information
    assert mesh.Box
    assert mesh.Mesh
    assert mesh.MeshBlock
    assert mesh.MeshLevel
    assert mesh.MeshVariable
    assert mesh.utils
