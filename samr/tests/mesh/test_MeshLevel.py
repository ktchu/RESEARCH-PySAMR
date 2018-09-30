"""
Unit tests for MeshLevel class

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
import numpy
import pytest

# XYZ
from samr.geometry import CartesianGeometry
from samr.mesh import Box
from samr.mesh import MeshLevel


# --- Tests

class MeshLevelTests(unittest.TestCase):
    """
    Unit tests for MeshLevel class.
    """
    # --- setUp/tearDown

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.boxes = [
            Box([0, 0], [9, 9]),
            Box([10, 5], [19, 14]),
            Box([0, 10], [4, 14]),
        ]

        self.x_lower = [0.0, 0.0]
        self.x_upper = [4.0, 3.0]
        self.geometry = CartesianGeometry(self.x_lower, self.x_upper)

    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(MeshLevel, 'level_number')
        assert hasattr(MeshLevel, 'blocks')
        assert hasattr(MeshLevel, 'num_blocks')
        assert hasattr(MeshLevel, 'variables')

    @unittest.skip('')
    def test_init_1(self):
        """
        Test construction of MeshLevel with default parameters.
        """
        # --- Exercise functionality

        level = MeshLevel(level_number=0,
                          boxes=self.boxes,
                          geometry=self.geometry)

        # --- Check results

        # level number
        assert level.level_number == 0

        # blocks
        # TODO
        # for idx, block in enumerate(level.blocks):
        #     assert block.box == self.boxes[idx]

        # variables
        assert isinstance(level.variables, tuple)
        assert not level.variables

    def test_init_2(self):
        """
        Test construction of MeshLevel: invalid 'level_number'
        """
        # level_number not a numeric value
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number='not numeric',
                          boxes=self.boxes,
                          geometry=self.geometry)

        expected_error = "'level_number' should be a numeric value"
        assert expected_error in str(exc_info)

        # level_number not an integer value
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=3.5,
                          boxes=self.boxes,
                          geometry=self.geometry)

        expected_error = "'level_number' should be an integer"
        assert expected_error in str(exc_info)

        # level_number < 0
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=-1,
                          boxes=self.boxes,
                          geometry=self.geometry)

        expected_error = "'level_number' should be a non-negative number"
        assert expected_error in str(exc_info)

    def test_init_3(self):
        """
        Test construction of MeshLevel: invalid 'boxes'
        """
        # --- Exercise functionality and check results

        # boxes is not a valid type
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=0,
                          boxes='invalid boxes',
                          geometry=self.geometry)

        expected_error = "'boxes' should be a Box or a list of Boxes"
        assert expected_error in str(exc_info)

        # empty boxes
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=0,
                          boxes=tuple(),
                          geometry=self.geometry)

        expected_error = "'boxes' should not be empty"
        assert expected_error in str(exc_info)

        # boxes contains non-Box item
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=0,
                          boxes=self.boxes + ['not a Box'],
                          geometry=self.geometry)

        expected_error = "'boxes' should not contain non-Box items"
        assert expected_error in str(exc_info)

    def test_init_4(self):
        """
        Test construction of MeshLevel: invalid 'geometry'
        """
        # geometry not a Geometry
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=3,
                          boxes=self.boxes,
                          geometry='not a Geometry')

        expected_error = "'geometry' should be a Geometry"
        assert expected_error in str(exc_info)
