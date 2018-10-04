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
import pytest

# XYZ
from samr.box import Box
from samr.geometry import CartesianGeometry
from samr.mesh import Mesh
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
        self.x_upper = [1.0, 1.0]
        self.first_box_geometry = CartesianGeometry(self.x_lower, self.x_upper)

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

    def test_init_1(self):
        """
        Test construction of MeshLevel with default parameters.
        """
        # --- Exercise functionality

        level = MeshLevel(0, self.boxes, self.first_box_geometry)

        # --- Check results

        # level number
        assert level.level_number == 0

        # block boxes
        for idx, block in enumerate(level.blocks):
            # Check that boxes are equivalent but not the same object
            assert block.box == self.boxes[idx]
            assert block.box is not self.boxes[idx]

        # block geometries
        assert level.blocks[0].geometry == self.first_box_geometry
        assert level.blocks[0].geometry is not self.first_box_geometry

        assert level.blocks[1].geometry == \
            CartesianGeometry([1.0, 0.5], [2.0, 1.5])
        assert level.blocks[2].geometry == \
            CartesianGeometry([0.0, 1.0], [0.5, 1.5])

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
                          first_box_geometry=self.first_box_geometry)

        expected_error = "'level_number' should be a numeric value"
        assert expected_error in str(exc_info)

        # level_number not an integer value
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=3.5,
                          boxes=self.boxes,
                          first_box_geometry=self.first_box_geometry)

        expected_error = "'level_number' should be an integer"
        assert expected_error in str(exc_info)

        # level_number < 0
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=-1,
                          boxes=self.boxes,
                          first_box_geometry=self.first_box_geometry)

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
                          first_box_geometry=self.first_box_geometry)

        expected_error = "'boxes' should be a Box or a list of Boxes"
        assert expected_error in str(exc_info)

        # empty boxes
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=0,
                          boxes=tuple(),
                          first_box_geometry=self.first_box_geometry)

        expected_error = "'boxes' should not be empty"
        assert expected_error in str(exc_info)

        # boxes contains non-Box item
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=0,
                          boxes=self.boxes + ['not a Box'],
                          first_box_geometry=self.first_box_geometry)

        expected_error = "'boxes' should not contain non-Box items"
        assert expected_error in str(exc_info)

    def test_init_4(self):
        """
        Test construction of MeshLevel: invalid 'first_box_geometry'
        """
        # first_box_geometry not a Geometry
        with pytest.raises(ValueError) as exc_info:
            _ = MeshLevel(level_number=3,
                          boxes=self.boxes,
                          first_box_geometry='not a Geometry')

        expected_error = "'first_box_geometry' should be a Geometry"
        assert expected_error in str(exc_info)

    def test_add_variable_1(self):
        """
        Test add_variable(): normal usage
        """
        # --- Preparations

        mesh = Mesh(self.boxes, self.first_box_geometry)

        variable = mesh.create_variable()

        level = MeshLevel(0, self.boxes, self.first_box_geometry)

        # --- Exercise functionality and check results

        level.add_variable(variable)

        assert variable in level.variables
        for block in level.blocks:
            assert variable in block.variables

    def test_add_variable_2(self):
        """
        Test add_variable(): invalid 'variable'
        """
        # --- Preparations

        level = MeshLevel(0, self.boxes, self.first_box_geometry)

        # --- Exercise functionality and check results

        # variable not a MeshVariable
        with pytest.raises(ValueError) as exc_info:
            level.add_variable('not a MeshVariable')

        expected_error = "'variable' should be a MeshVariable"
        assert expected_error in str(exc_info)

    def test_generate_blocks_1(self):
        """
        Test _generate_blocks(): normal usage
        """
        # pylint: disable=protected-access

        # --- Preparations

        blocks = \
            MeshLevel._generate_blocks(self.boxes, self.first_box_geometry)

        # --- Exercise functionality and check results

        # block boxes
        for idx, block in enumerate(blocks):
            # Check that boxes are equivalent but not the same object
            assert block.box == self.boxes[idx]
            assert block.box is not self.boxes[idx]

        # block Geometries
        assert blocks[0].geometry == self.first_box_geometry
        assert blocks[0].geometry is not self.first_box_geometry

        assert blocks[1].geometry == CartesianGeometry([1.0, 0.5], [2.0, 1.5])
        assert blocks[2].geometry == CartesianGeometry([0.0, 1.0], [0.5, 1.5])

    def test_generate_blocks_2(self):
        """
        Test _generate_blocks(): invalid parameters
        """
        # pylint: disable=protected-access

        # --- Exercise functionality and check results

        # boxes is not list-like
        with pytest.raises(ValueError) as exc_info:
            MeshLevel._generate_blocks(
                boxes='not a list of boxes',
                first_box_geometry=self.first_box_geometry)

        expected_error = "'boxes' should be a list of Boxes"
        assert expected_error in str(exc_info)

        # boxes is empty
        with pytest.raises(ValueError) as exc_info:
            MeshLevel._generate_blocks(
                boxes=[], first_box_geometry=self.first_box_geometry)

        expected_error = "'boxes' should not be empty"
        assert expected_error in str(exc_info)

        # boxes contains non-Box items
        with pytest.raises(ValueError) as exc_info:
            MeshLevel._generate_blocks(
                boxes=self.boxes + ['not a Box'],
                first_box_geometry=self.first_box_geometry)

        expected_error = "'boxes' should not contain non-Box items"
        assert expected_error in str(exc_info)

        # first_box_geometry not a Geometry
        with pytest.raises(ValueError) as exc_info:
            MeshLevel._generate_blocks(boxes=self.boxes, first_box_geometry=1)

        expected_error = "'first_box_geometry' should be a Geometry"
        assert expected_error in str(exc_info)

    def test_repr(self):
        """
        Test __repr__().
        """
        # --- Preparations

        mesh = Mesh(self.boxes, self.first_box_geometry)

        variable = mesh.create_variable()

        level = MeshLevel(0, self.boxes, self.first_box_geometry)

        level.add_variable(variable)

        # --- Exercise functionality and check results

        expected_repr = "MeshLevel(level_number=0, blocks={}, variables={})". \
            format(list(level.blocks), list(mesh.variables))

        assert repr(level) == expected_repr
        assert str(level) == expected_repr
