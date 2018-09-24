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
import pytest

# XYZ
from samr.geometry import CartesianGeometry
from samr.mesh import Box
from samr.mesh import Mesh


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
        self.num_dimensions = 3

        lower = [1] * self.num_dimensions
        upper = [100] * self.num_dimensions
        self.domain = [Box(lower, upper)]

        self.x_lower = [0] * self.num_dimensions
        self.dx = [0.1] * self.num_dimensions
        self.geometry = CartesianGeometry(self.x_lower, self.dx)

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

        assert hasattr(Mesh, 'data')

        assert hasattr(Mesh, 'is_single_level')
        assert hasattr(Mesh, 'is_single_block')

        assert hasattr(Mesh, 'add_level')

    def test_init_1(self):
        """
        Test __init__(): valid parameters for single-block Mesh
        """
        # --- Exercise functionality and check results

        # ------ single_block=True, single_level not set

        # Create mesh
        mesh = Mesh(self.domain, self.geometry, single_block=True)

        # Check that domain is equivalent and is a copy (not the same object)
        assert mesh.domain == self.domain
        assert mesh.domain is not self.domain

        # Check that each box is equivalent and is a copy (not the same object)
        for idx, box in enumerate(mesh.domain):
            assert box == self.domain[idx]
            assert box is not self.domain[idx]

        # Check bounding box
        assert mesh.bounding_box == self.domain[0]

        # Check that geometry is equivalent and is a copy (not the same object)
        assert mesh.geometry == self.geometry
        assert mesh.geometry is not self.geometry

        assert mesh.num_dimensions == self.geometry.num_dimensions

        # Check levels
        assert len(mesh.levels) == 1
        assert mesh.num_levels == 1

        # Check blocks
        assert len(mesh.blocks) == 1
        assert mesh.num_blocks == 1

        # Check is_single_level and is_single_block
        assert mesh.is_single_level
        assert mesh.is_single_block

        # ------ single_block=True, single_level=False

        # Create mesh
        mesh = Mesh(self.domain, self.geometry,
                    single_block=True, single_level=False)

        # Check is_single_level and is_single_block
        assert mesh.is_single_level
        assert mesh.is_single_block

    def test_init_5(self):
        """
        Test __init__(): invalid 'domain'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(self.domain, geometry='not a Geometry object')

        expected_error = "'geometry' is not a Geometry object"
        assert expected_error in str(exc_info)

    def test_init_6(self):
        """
        Test __init__(): invalid 'geometry'
        """
        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(self.domain, geometry='not a Geometry object')

        expected_error = "'geometry' is not a Geometry object"
        assert expected_error in str(exc_info)
