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
import samr.box
import samr.geometry
import samr.mesh
import samr.utils


# --- Tests

def test_package_info_attributes():
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


def test_packages_and_modules():
    """
   Test for expected packages and modules.
    """
    # Packages
    assert samr.box
    assert samr.geometry
    assert samr.mesh

    # Modules
    assert samr.utils
