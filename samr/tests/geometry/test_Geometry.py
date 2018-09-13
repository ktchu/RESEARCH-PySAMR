"""
Unit tests Geometry class

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
from samr.geometry import Geometry


# --- Tests

class GeometryTests(unittest.TestCase):
    """
    Unit tests for Geometry class.
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(Geometry, 'num_dimensions')

    @staticmethod
    def test_init_1():
        """
        Test construction of Geometry object with valid parameters.
        """
        # Exercise functionality
        num_dimensions = 3
        geometry = Geometry(num_dimensions)

        # Check results
        assert geometry.num_dimensions == num_dimensions

    @staticmethod
    def test_init_2():
        """
        Test construction of Geometry object. Invalid 'num_dimensions'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = Geometry(num_dimensions='not an int')

        if exc_info:
            expected_error = "'num_dimensions' is not an integer"
        assert expected_error in str(exc_info)

        # num_dimensions = 0
        with pytest.raises(ValueError) as exc_info:
            _ = Geometry(num_dimensions=0)

        if exc_info:
            expected_error = "'num_dimensions' is not a positive integer"
        assert expected_error in str(exc_info)

        # num_dimensions < 0
        with pytest.raises(ValueError) as exc_info:
            _ = Geometry(num_dimensions=-1)

        if exc_info:
            expected_error = "'num_dimensions' is not a positive integer"
        assert expected_error in str(exc_info)
