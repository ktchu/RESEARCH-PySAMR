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
        self.x_lower = numpy.zeros(self.num_dimensions)
        self.dx = 0.1 * numpy.ones(self.num_dimensions)
        self.geometry = CartesianGeometry(self.num_dimensions,
                                          self.x_lower, self.dx)

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

        assert hasattr(MeshBlock, 'data')

    def test_init_1(self):
        """
        Test construction of MeshBlock object with valid parameters.
        """
        # Exercise functionality

        block = MeshBlock(self.box, self.geometry)

        # Check results

        assert block.num_dimensions == self.num_dimensions

        assert block.box == self.box

        assert numpy.array_equal(block.lower, self.lower)
        assert block.lower.dtype == numpy.int64

        assert numpy.array_equal(block.upper, self.upper)
        assert block.upper.dtype == numpy.int64

        assert numpy.array_equal(block.shape, self.box.shape)
        assert block.size == self.box.size

        assert block.geometry == self.geometry

        assert block.data == {}

    def test_init_2(self):
        """
        Test construction of MeshBlock object. Invalid 'box'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(box='not a Box object', geometry=self.geometry)

        if exc_info:
            expected_error = "'box' is not a Box object"
        assert expected_error in str(exc_info)

    def test_init_3(self):
        """
        Test construction of MeshBlock object. Invalid 'geometry'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(self.box, geometry='not a Geometry object')

        if exc_info:
            expected_error = "'geometry' is not a Geometry object"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_add_variable(self):
        """
        Test addition of MeshVariable to MeshBlock.
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
        Test addition of MeshVariable to MeshBlock.
        """
        # Preparations
        block = MeshBlock(self.box, self.geometry)

        # Exercise functionality
        # TODO

        # Check results
        # TODO
