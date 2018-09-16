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
from samr.geometry import CartesianGeometry
from samr.mesh import Mesh
from samr.mesh import MeshBlock


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
        self.x_lower = numpy.zeros(self.num_dimensions)
        self.dx = 0.1*numpy.ones(self.num_dimensions)
        self.geometry = CartesianGeometry(self.num_dimensions,
                                          self.x_lower,
                                          self.dx)

    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(Mesh, 'num_dimensions')
        assert hasattr(Mesh, 'geometry')
        assert hasattr(Mesh, 'domain')
        assert hasattr(Mesh, 'domain_block')

        assert hasattr(Mesh, 'levels')
        assert hasattr(Mesh, 'blocks')

    def test_init_1(self):
        """
        Test construction of Mesh object with valid parameters.
        """
        # Exercise functionality
        lower = numpy.ones(self.num_dimensions, dtype='int')
        upper = 100 * numpy.ones(self.num_dimensions, dtype='int')
        mesh = Mesh(self.geometry, lower, upper)

        # Check results
        assert mesh.num_dimensions == self.num_dimensions
        assert mesh.geometry == self.geometry
        assert mesh.domain is None

        expected_domain_block = MeshBlock(self.geometry, lower, upper)
        assert mesh.domain_block.geometry == expected_domain_block.geometry
        assert numpy.all(
            mesh.domain_block.lower == expected_domain_block.lower)
        assert numpy.all(
            mesh.domain_block.upper == expected_domain_block.upper)

        assert mesh.levels == []

        with pytest.raises(RuntimeError) as exc_info:
            _ = mesh.blocks

        if exc_info:
            expected_error = "Mesh contains no blocks"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_init_2(self):
        """
        Test construction of MeshBlock object. Invalid 'geometry'
        """
        # --- Preparations

        lower = numpy.ones(self.num_dimensions, dtype='int')
        upper = 100 * numpy.ones(self.num_dimensions, dtype='int')

        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry='not a Geometry object',
                          lower=lower, upper=upper)

        if exc_info:
            expected_error = "'geometry' is not Geometry object"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_init_3(self):
        """
        Test construction of MeshBlock object. Invalid 'lower'
        """
        # --- Preparations

        upper = numpy.ones(self.num_dimensions)

        # --- Exercise functionality and check results

        # lower not a numpy.ndarray
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry=self.geometry,
                          lower=3,
                          upper=upper)

        if exc_info:
            expected_error = "'lower' is not a numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(lower) != num_dimensions
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry=self.geometry,
                          lower=numpy.zeros(self.num_dimensions-1,
                                            dtype='int'),
                          upper=upper)

        if exc_info:
            expected_error = "'lower' does not have 'num_dimensions' " \
                             "components"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_init_4(self):
        """
        Test construction of MeshBlock object. Invalid 'upper'
        """
        # --- Preparations

        lower = numpy.zeros(self.num_dimensions, dtype='int')

        # --- Exercise functionality and check results

        # upper not a numpy.ndarray
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry=self.geometry,
                          lower=lower,
                          upper='not a numpy.ndarray')

        if exc_info:
            expected_error = "'upper' is not a numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(upper) != num_dimensions
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry=self.geometry,
                          lower=lower,
                          upper=numpy.ones(self.num_dimensions+1,
                                           dtype='int'))

        if exc_info:
            expected_error = "'upper' does not have 'num_dimensions' " \
                             "components"
        assert expected_error in str(exc_info)

    @unittest.skip('TODO')
    def test_init_5(self):
        """
        Test construction of MeshBlock object. 'upper' not greater than 'lower'
        """
        # --- Preparations

        lower = numpy.ones(self.num_dimensions, dtype='int')
        upper = 10 * numpy.ones(self.num_dimensions, dtype='int')
        upper[1] = 0

        # --- Exercise functionality and check results

        # upper not a numpy.ndarray
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry=self.geometry,
                          lower=lower, upper=upper)

        if exc_info:
            expected_error = \
                "Some components of 'upper' are less than or equal " \
                "to components of 'lower'"
        assert expected_error in str(exc_info)
