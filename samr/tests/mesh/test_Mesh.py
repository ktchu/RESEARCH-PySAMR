"""
Unit tests for Mesh class

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
from samr.mesh import MeshVariable


# --- Tests

class MeshTests(unittest.TestCase):
    """
    Unit tests for Mesh class.
    """
    # --- setUp/tearDown

    def setUp(self):
        """
        Set up test fixtures.
        """
        self.domain = [
            Box([0, 0], [9, 9]),
            Box([10, 5], [19, 14]),
            Box([0, 10], [4, 14]),
        ]

        self.x_lower = [0.0, 0.0]
        self.x_upper = [1.0, 1.0]
        self.first_box_geometry = CartesianGeometry(self.x_lower, self.x_upper)

        self.num_dimensions = self.first_box_geometry.num_dimensions

    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(Mesh, 'domain')
        assert hasattr(Mesh, 'bounding_box')
        assert hasattr(Mesh, 'geometry')
        assert hasattr(Mesh, 'num_dimensions')

        assert hasattr(Mesh, 'levels')
        assert hasattr(Mesh, 'num_levels')

        assert hasattr(Mesh, 'blocks')
        assert hasattr(Mesh, 'num_blocks')
        assert hasattr(Mesh, 'block')

        assert hasattr(Mesh, 'variables')

        assert hasattr(Mesh, 'is_single_level')
        assert hasattr(Mesh, 'is_single_block')

        assert hasattr(Mesh, 'create_variable')

        assert hasattr(Mesh, 'add_level')
        assert hasattr(Mesh, 'remove_level')

        assert hasattr(Mesh, 'data')

    def test_init_1(self):
        """
        Test __init__(): valid parameters for Mesh multi-box domain
        """
        # --- Exercise functionality and check results

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # domain is equivalent and is a copy (not the same object)
        assert isinstance(mesh.domain, tuple)
        assert mesh.domain == tuple(self.domain)
        assert mesh.domain is not self.domain

        # boxes are equivalent and are copies (not the same object)
        for idx, box in enumerate(mesh.domain):
            assert box == self.domain[idx]
            assert box is not self.domain[idx]

        # bounding box
        expected_bounding_box = Box.compute_bounding_box(self.domain)
        assert mesh.bounding_box == expected_bounding_box

        # geometry
        x_lower = [0.0, 0.0]
        x_upper = [2.0, 1.5]
        assert mesh.geometry == CartesianGeometry(x_lower, x_upper)

        # num_dimensions
        assert mesh.num_dimensions == self.num_dimensions

        # levels
        assert isinstance(mesh.levels, tuple)
        assert len(mesh.levels) == 1
        assert mesh.num_levels == 1

        # blocks
        assert isinstance(mesh.blocks, tuple)
        assert len(mesh.blocks) == 3
        assert mesh.num_blocks == 3

        # variables
        assert isinstance(mesh.variables, tuple)
        assert not mesh.variables

        # is single-level
        assert mesh.is_single_level

        # is not single-block
        assert not mesh.is_single_block

    @staticmethod
    def test_init_2():
        """
        Test __init__(): valid parameters for single-block Mesh
        """
        # --- Preparations

        num_dimensions = 5
        lower = [1] * num_dimensions
        upper = [100] * num_dimensions
        domain = Box(lower, upper)

        x_lower = [0.0] * num_dimensions
        x_upper = [1.0] * num_dimensions
        geometry = CartesianGeometry(x_lower, x_upper)

        # --- Exercise functionality and check results

        # ------ single-level Mesh

        # Create mesh
        mesh = Mesh(domain, geometry)

        # domain is equivalent and is a copy (not the same object)
        assert mesh.domain == tuple([domain])

        # domain box is equivalent and is a copy (not the same object)
        assert mesh.domain[0] == domain
        assert mesh.domain[0] is not domain

        # bounding box
        assert mesh.bounding_box == domain

        # geometry is equivalent and is a copy (not the same object)
        assert mesh.geometry == geometry
        assert mesh.geometry is not geometry

        assert mesh.num_dimensions == geometry.num_dimensions

        # levels
        assert len(mesh.levels) == 1
        assert mesh.num_levels == 1

        # blocks
        assert len(mesh.blocks) == 1
        assert mesh.num_blocks == 1

        # is single-level
        assert mesh.is_single_level

        # is single-block
        assert mesh.is_single_block

    def test_init_3(self):
        """
        Test __init__(): invalid parameters
        """
        # --- Exercise functionality and check results

        # domain is not a valid type
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(domain='invalid domain',
                     first_box_geometry=self.first_box_geometry)

        expected_error = "'domain' should be a Box or a list of Boxes"
        assert expected_error in str(exc_info)

        # empty domain
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(domain=[], first_box_geometry=self.first_box_geometry)

        expected_error = "'domain' should not be empty"
        assert expected_error in str(exc_info)

        # domain contains non-Box item
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(domain=self.domain + ['not a Box'],
                     first_box_geometry=self.first_box_geometry)

        expected_error = "'domain' should not contain non-Box items"
        assert expected_error in str(exc_info)

        # invalid first_box_geometry
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(self.domain, first_box_geometry='not a Geometry')

        expected_error = "'first_box_geometry' should be a Geometry"
        assert expected_error in str(exc_info)

    def test_create_variable_1(self):
        """
        Test create_variable(): normal usage
        """
        # ------ Preparations

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # Add levels to Mesh
        # TODO

        # --- Exercise functionality and check results

        # ------ Default variable parameters

        # Create variable
        variable = mesh.create_variable()

        # Check that 'variable' is a MeshVariable
        assert isinstance(variable, MeshVariable)

        # Check 'variable' properties
        assert variable.mesh == mesh
        assert variable.location == MeshVariable.Location.NODE
        assert numpy.array_equal(variable.max_stencil_width,
                                 numpy.zeros(mesh.num_dimensions))
        assert variable.depth == 1
        assert variable.dtype == numpy.float64

        # Check that 'variable' has been added to Mesh, MeshLevels,
        # and MeshBlocks
        assert variable in mesh.variables
        for level in mesh.levels:
            assert variable in level.variables
            for block in level.blocks:
                assert variable in block.variables

        # ------ Custom variable parameters #1

        # Create variable
        variable = mesh.create_variable(
            location=MeshVariable.Location.CELL,
            max_stencil_width=2,
            precision=MeshVariable.Precision.SINGLE)

        # Check that 'variable' is a MeshVariable
        assert isinstance(variable, MeshVariable)

        # Check 'variable' properties
        assert variable.mesh == mesh
        assert variable.location == MeshVariable.Location.CELL
        assert numpy.array_equal(variable.max_stencil_width,
                                 2 * numpy.ones(mesh.num_dimensions))
        assert variable.depth == 1
        assert variable.dtype == numpy.float32

        # Check that 'variable' has been added to Mesh, MeshLevels,
        # and MeshBlocks
        assert variable in mesh.variables
        for level in mesh.levels:
            assert variable in level.variables
            for block in level.blocks:
                assert variable in block.variables

        # ------ Custom variable parameters #2

        # Create variable
        variable = mesh.create_variable(max_stencil_width=1, depth=5)

        # Check that 'variable' is a MeshVariable
        assert isinstance(variable, MeshVariable)

        # Check 'variable' properties
        assert variable.mesh == mesh
        assert variable.location == MeshVariable.Location.NODE
        assert numpy.array_equal(variable.max_stencil_width,
                                 numpy.ones(mesh.num_dimensions))
        assert variable.depth == 5
        assert variable.dtype == numpy.float64

        # Check that 'variable' has been added to Mesh, MeshLevels,
        # and MeshBlocks
        assert variable in mesh.variables
        for level in mesh.levels:
            assert variable in level.variables
            for block in level.blocks:
                assert variable in block.variables

    def test_create_variable_2(self):
        """
        Test create_variables(): invalid parameters
        """
        # --- Preparations

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # --- Exercise functionality and check results

        # level_numbers is an empty array
        with pytest.raises(ValueError) as exc_info:
            mesh.create_variable(level_numbers=[])

        expected_error = "'level_numbers' should not be empty"
        assert expected_error in str(exc_info)

        # level_numbers is not a scalar and not list-like
        with pytest.raises(ValueError) as exc_info:
            mesh.create_variable(level_numbers='invalid level_numbers')

        expected_error = "'level_numbers' should be a scalar, a " \
                         "list-like collection of integers, or a " \
                         "numpy.ndarray"
        assert expected_error in str(exc_info)

        # level_numbers contains non-integer values
        with pytest.raises(ValueError) as exc_info:
            mesh.create_variable(level_numbers=[1, 2.5])

        expected_error = "'level_numbers' should contain only integer values"
        assert expected_error in str(exc_info)

        # level_numbers contains negative values
        with pytest.raises(ValueError) as exc_info:
            mesh.create_variable(level_numbers=[-2, 0, 1])

        expected_error = "'level_numbers' should not contain negative values"
        assert expected_error in str(exc_info)

        # level_numbers contains values that exceed (mesh.num_levels - 1)
        with pytest.raises(ValueError) as exc_info:
            mesh.create_variable(level_numbers=[0, mesh.num_levels])

        expected_error = "'level_numbers' should only contain values " \
                         "less than number of levels in the Mesh"
        assert expected_error in str(exc_info)

    @unittest.skip("TODO")
    def test_add_level(self):
        """
        Test add_level()
        """
        # ------ Preparations

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # Add levels to Mesh
        # TODO

        # --- Exercise functionality and check results

        # TODO

    @unittest.skip("TODO")
    def test_remove_level_1(self):
        """
        Test remove_level(): normal usage
        """
        # ------ Preparations

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # Add levels to Mesh
        # TODO

        # --- Exercise functionality and check results

        # TODO

    def test_remove_level_2(self):
        """
        Test remove_level(): Mesh contains only coarsest MeshLevel
        """
        # ------ Preparations

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # --- Exercise functionality and check results

        with pytest.raises(RuntimeError) as exc_info:
            mesh.remove_level()

        expected_error = "The coarsest MeshLevel cannot be removed from Mesh"
        assert expected_error in str(exc_info)

    def test_repr(self):
        """
        Test __repr__()
        """
        # ------ Preparations

        # Create mesh
        mesh = Mesh(self.domain, self.first_box_geometry)

        # Add levels to Mesh
        # TODO

        # Add variables to Mesh
        # TODO

        # --- Exercise functionality and check results

        expected_repr = "Mesh(domain={}, levels={}, variables={}, " \
            "single_level=True, single_block=False)".format(
                list(mesh.domain), list(mesh.levels), list(mesh.variables))
        assert repr(mesh) == expected_repr
        assert str(mesh) == expected_repr
