"""
Unit tests for top-level of XYZ package.

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
import samr


# --- Tests

def test_attributes():
    """
   Test for expected package attributes.
    """
    # Package information
    assert samr.__version__
    assert hasattr(samr, '__author__')
    assert hasattr(samr, '__author_email__')
    assert samr.__license__
    assert samr.__copyright__

    assert not hasattr(samr, '_PKG_INFO')


def test_subpackages():
    """
   Test for expected sub-packages.
    """
    assert samr.geometry
    assert samr.mesh
