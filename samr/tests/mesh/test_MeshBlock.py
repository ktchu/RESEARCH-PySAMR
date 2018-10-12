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
from samr.box import Box
from samr.geometry import CartesianGeometry
from samr.mesh import Mesh
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

        assert hasattr(MeshBlock, 'num_dimensions')
        assert hasattr(MeshBlock, 'lower')
        assert hasattr(MeshBlock, 'upper')
        assert hasattr(MeshBlock, 'shape')
        assert hasattr(MeshBlock, 'size')

        assert hasattr(MeshBlock, 'variables')

        # Methods
        assert hasattr(MeshBlock, 'add_variable')
        assert hasattr(MeshBlock, 'data')

    def test_init_1(self):
        """
        Test __init__(): valid parameters
        """
        # --- Exercise functionality

        block = MeshBlock(self.box, self.geometry)

        # --- Check results

        # box is equivalent and is a copy (not the same object)
        assert block.box == self.box
        assert block.box is not self.box

        # geometry is equivalent and is a copy (not the same object)
        assert block.geometry == self.geometry
        assert block.geometry is not self.geometry

        # num_dimensions
        assert block.num_dimensions == self.num_dimensions

        # index space
        assert numpy.array_equal(block.lower, self.lower)
        assert block.lower.dtype == numpy.int64
        assert numpy.array_equal(block.upper, self.upper)
        assert block.upper.dtype == numpy.int64

        # shape and size
        assert numpy.array_equal(block.shape, self.box.shape)
        assert block.size == self.box.size

        # variables
        assert block.variables == tuple()

        # data
        assert block.data() == {}

    def test_init_2(self):
        """
        Test __init__(): invalid parameters
        """
        # --- Exercise functionality and check results

        # 'box' is not a Box
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(box='not a Box', geometry=self.geometry)

        expected_error = "'box' should be a Box"
        assert expected_error in str(exc_info)

        # 'geometry' is not a Geometry
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(self.box, geometry='not a Geometry')

        expected_error = "'geometry' should be a Geometry"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_3():
        """
        Test __init__(): incompatible 'box' and 'geometry'
        """
        # --- Exercise functionality and check results

        num_dimensions = 2
        lower = [0] * num_dimensions
        upper = [99] * num_dimensions
        box = Box(lower, upper)

        x_lower = [0] * (num_dimensions + 1)
        x_upper = [1] * (num_dimensions + 1)
        geometry = CartesianGeometry(x_lower, x_upper)

        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(box, geometry)

        expected_error = "'box' and 'geometry' should have the same " \
                         "number of dimensions"
        assert expected_error in str(exc_info)

    def test_add_variable_1(self):
        """
        Test add_variable(): normal usage
        """
        # --- Preparations

        mesh = Mesh(self.box, self.geometry)

        variable_1 = mesh.create_variable()
        variable_2 = mesh.create_variable()

        block = MeshBlock(self.box, self.geometry)

        # --- Exercise functionality and check results

        # Add variable_1
        block.add_variable(variable_1)

        assert variable_1 in block.variables
        assert len(block.variables) == 1
        assert id(variable_1) \
            in block._data  # pylint: disable=protected-access

        # Add variable_2
        block.add_variable(variable_2)

        assert variable_2 in block.variables
        assert len(block.variables) == 2
        assert id(variable_2) \
            in block._data  # pylint: disable=protected-access

        # Re-add variable_2
        block.add_variable(variable_2)

        assert len(block.variables) == 2
        assert id(variable_2) \
            in block._data  # pylint: disable=protected-access

    def test_add_variable_2(self):
        """
        Test add_variable(): invalid 'variable'
        """
        # --- Preparations

        block = MeshBlock(self.box, self.geometry)

        # --- Exercise functionality and check results

        with pytest.raises(ValueError) as exc_info:
            block.add_variable('Not a MeshVariable')

        expected_error = "'variable' should be a MeshVariable"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_data(self):
        """
        Test data(): normal usage
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

        mesh = Mesh(self.box, self.geometry)

        variable = mesh.create_variable()

        block = MeshBlock(self.box, self.geometry)
        block.add_variable(variable)

        # --- Exercise functionality and check results

        expected_repr = "MeshBlock(" \
                        "box=Box([1, 1, 1], [100, 100, 100]), " \
                        "geometry=CartesianGeometry([0.0, 0.0, 0.0], " \
                        "[1.0, 1.0, 1.0]), " \
                        "variables={})".format(list(block.variables))
        assert repr(block) == expected_repr
        assert str(block) == expected_repr
