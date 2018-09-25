"""
Unit tests for MeshBlock class

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
from samr.mesh import MeshBlock


# --- Tests

class MeshBlockTests(unittest.TestCase):
    """
    Unit tests for MeshBlock class.
    """
    # --- setUp/tearDown

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.num_dimensions = 3

        # box
        self.lower = [1] * self.num_dimensions
        self.upper = [100] * self.num_dimensions
        self.box = Box(self.lower, self.upper)

        # geometry
        self.x_lower = [0] * self.num_dimensions
        self.x_upper = [1] * self.num_dimensions
        self.geometry = CartesianGeometry(self.x_lower, self.x_upper)

    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(MeshBlock, 'box')
        assert hasattr(MeshBlock, 'geometry')

        assert hasattr(MeshBlock, 'lower')
        assert hasattr(MeshBlock, 'upper')
        assert hasattr(MeshBlock, 'num_dimensions')
        assert hasattr(MeshBlock, 'shape')
        assert hasattr(MeshBlock, 'size')

        assert hasattr(MeshBlock, 'variables')
        assert hasattr(MeshBlock, 'data')

        # Methods
        assert hasattr(MeshBlock, 'add_variable')
        assert hasattr(MeshBlock, 'get_data')

    def test_init_1(self):
        """
        Test __init__(): valid parameters
        """
        # --- Exercise functionality

        block = MeshBlock(self.box, self.geometry)

        # --- Check results

        # num_dimensions
        assert block.num_dimensions == self.num_dimensions

        # box is equivalent and is a copy (not the same object)
        assert block.box == self.box
        assert block.box is not self.box

        assert numpy.array_equal(block.lower, self.lower)
        assert block.lower.dtype == numpy.int64

        assert numpy.array_equal(block.upper, self.upper)
        assert block.upper.dtype == numpy.int64

        assert numpy.array_equal(block.shape, self.box.shape)
        assert block.size == self.box.size

        # geometry is equivalent and is a copy (not the same object)
        assert block.geometry == self.geometry
        assert block.geometry is not self.geometry

        assert block.data == {}

    def test_init_2(self):
        """
        Test __init__(): invalid 'box'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(box='not a Box object', geometry=self.geometry)

        expected_error = "'box' is not a Box object"
        assert expected_error in str(exc_info)

    def test_init_3(self):
        """
        Test __init__(): invalid 'geometry'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(self.box, geometry='not a Geometry object')

        expected_error = "'geometry' is not a Geometry object"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_add_variable_1(self):
        """
        Test add_variable(): normal usage
        """
        # Preparations
        block = MeshBlock(self.box, self.geometry)

        # Exercise functionality
        # TODO

        # Check results
        # TODO

    @unittest.skip('TODO')
    def test_get_data(self):
        """
        Test get_data(): normal usage
        """
        # Preparations
        block = MeshBlock(self.box, self.geometry)

        # Exercise functionality
        # TODO

        # Check results
        # TODO

    def test_repr(self):
        """
        Test __repr__().
        """
        # --- Preparations

        block = MeshBlock(self.box, self.geometry)

        # --- Exercise functionality and check results

        expected_repr = "MeshBlock(" \
                        "box=Box([1, 1, 1], [100, 100, 100]), " \
                        "geometry=CartesianGeometry([0.0, 0.0, 0.0], " \
                        "[1.0, 1.0, 1.0]), " \
                        "variables=())"
        assert repr(block) == expected_repr
        assert str(block) == expected_repr
