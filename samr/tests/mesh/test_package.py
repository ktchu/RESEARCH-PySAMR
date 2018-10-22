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

def test_types():
    """
    Test for expected types.
    """
    assert mesh.Mesh
    assert isinstance(mesh.Mesh, type)
    assert mesh.MeshBlock
    assert isinstance(mesh.MeshBlock, type)
    assert mesh.MeshLevel
    assert isinstance(mesh.MeshLevel, type)
    assert mesh.MeshVariable
