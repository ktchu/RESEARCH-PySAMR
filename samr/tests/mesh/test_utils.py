"""
Unit tests for mesh.utils module

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
import unittest

# External packages
import pytest

# XYZ
from samr.mesh import utils


# --- Tests

class mesh_utils_Tests(unittest.TestCase):
    """
    Unit tests for mesh.utils module
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Public functions
        assert hasattr(utils, 'contains_only_integers')

    @staticmethod
    def test_contains_only_integers():
        """
        Test contains_only_integers().
        """
        # pylint: disable=protected-access

        # --- Exercise functionality and check results

        # Normal usage
        assert utils.contains_only_integers([1, 2, 3])
        assert not utils.contains_only_integers([1, 2, 3.4])
        assert utils.contains_only_integers(1)
        assert not utils.contains_only_integers(1.5)

        # 'array' is not a scalar or array-like
        with pytest.raises(ValueError) as exc_info:
            utils.contains_only_integers('invalid array')

        expected_error = "'array' is not a scalar, list, tuple, or " \
                         "numpy.ndarray"
        assert expected_error in str(exc_info)

        # 'array' contains values that cannot be converted to a numeric value
        # 'array' cannot be converted to an array of numeric values
        with pytest.raises(ValueError) as exc_info:
            utils.contains_only_integers([1, 2, 2.5, 'non-numeric'])

        expected_error = "Unable to convert 'array' to an array of " \
                         "numeric values"
        assert expected_error in str(exc_info)
