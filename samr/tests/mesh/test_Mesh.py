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
        self.domain = [
            Box([0, 0], [10, 10]),
            Box([10, 5], [20, 15]),
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
        assert hasattr(Mesh, 'domain')
        assert hasattr(Mesh, 'bounding_box')
        assert hasattr(Mesh, 'geometry')
        assert hasattr(Mesh, 'num_dimensions')

        assert hasattr(Mesh, 'levels')
        assert hasattr(Mesh, 'num_levels')

        assert hasattr(Mesh, 'blocks')
        assert hasattr(Mesh, 'num_blocks')

        assert hasattr(Mesh, 'variables')

        assert hasattr(Mesh, 'is_single_level')
        assert hasattr(Mesh, 'is_single_block')

        assert hasattr(Mesh, 'add_level')
        assert hasattr(Mesh, 'create_variable')

        assert hasattr(Mesh, 'data')

    def test_init_1(self):
        """
        Test __init__(): valid parameters for Mesh multi-box domain
        """
        # --- Exercise functionality and check results

        # ------ single-level Mesh

        # Create mesh
        mesh = Mesh(self.domain, self.geometry, single_level=True)

        # domain is equivalent and is a copy (not the same object)
        assert mesh.domain == self.domain
        assert mesh.domain is not self.domain

        # boxes are equivalent and are copies (not the same object)
        for idx, box in enumerate(mesh.domain):
            assert box == self.domain[idx]
            assert box is not self.domain[idx]

        # bounding box
        expected_bounding_box = Box.compute_bounding_box(self.domain)
        assert mesh.bounding_box == expected_bounding_box

        # geometry is equivalent and is a copy (not the same object)
        assert mesh.geometry == self.geometry
        assert mesh.geometry is not self.geometry

        assert mesh.num_dimensions == self.geometry.num_dimensions

        # levels
        assert len(mesh.levels) == 1
        assert mesh.num_levels == 1

        # blocks
        assert len(mesh.blocks) == 2
        assert mesh.num_blocks == 2

        # is single-level
        assert mesh.is_single_level

        # is not single-block
        assert not mesh.is_single_block

        # ------ multi-level Mesh

        # Create mesh
        mesh = Mesh(self.domain, self.geometry, single_level=False)

        # is single-level
        assert not mesh.is_single_level

        # is single-block
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
        mesh = Mesh(domain, geometry, single_level=True)

        # domain is equivalent and is a copy (not the same object)
        assert mesh.domain == [domain]

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

        # ------ multi-level Mesh

        # Create mesh
        mesh = Mesh(domain, geometry, single_level=False)

        # is single-level
        assert not mesh.is_single_level

        # is single-block
        assert not mesh.is_single_block

    def test_init_3(self):
        """
        Test __init__(): invalid 'domain'
        """
        # --- Exercise functionality and check results

        # domain is not a valid type
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(domain='invalid domain', geometry=self.geometry)

        expected_error = "'domain' is not a Box object or a list of Box " \
                         "objects"
        assert expected_error in str(exc_info)

        # empty domain
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(domain=[], geometry=self.geometry)

        expected_error = "'domain' is empty"
        assert expected_error in str(exc_info)

        # domain contains non-Box object
        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(domain=self.domain + ['not a Box'],
                     geometry=self.geometry)

        expected_error = "'domain' contains a non-Box object"
        assert expected_error in str(exc_info)

    def test_init_4(self):
        """
        Test __init__(): invalid 'geometry'
        """
        # --- Exercise functionality and check results

        with pytest.raises(ValueError) as exc_info:
            _ = Mesh(self.domain, geometry='not a Geometry object')

        expected_error = "'geometry' is not a Geometry object"
        assert expected_error in str(exc_info)
