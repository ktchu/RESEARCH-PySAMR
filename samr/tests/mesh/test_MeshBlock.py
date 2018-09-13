"""
Unit tests MeshBlock class

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
        assert hasattr(MeshBlock, 'num_dimensions')
        assert hasattr(MeshBlock, 'lower')
        assert hasattr(MeshBlock, 'upper')

    def test_init_1(self):
        """
        Test construction of MeshBlock object with valid parameters.
        """
        # Exercise functionality
        lower = numpy.zeros(self.num_dimensions, dtype='int')
        upper = numpy.ones(self.num_dimensions, dtype='int')
        block = MeshBlock(self.geometry, lower, upper)

        # Check results
        assert block.num_dimensions == self.num_dimensions
        assert numpy.array_equal(block.lower, lower)
        assert block.lower.dtype == numpy.int64
        assert numpy.array_equal(block.upper, upper)
        assert block.upper.dtype == numpy.int64

    def test_init_2(self):
        """
        Test construction of MeshBlock object. Invalid 'geometry'
        """
        # --- Preparations

        lower = numpy.zeros(self.num_dimensions, dtype='int')
        upper = numpy.ones(self.num_dimensions, dtype='int')

        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = MeshBlock(geometry='not a Geometry object',
                          lower=lower, upper=upper)

        if exc_info:
            expected_error = "'geometry' is not Geometry object"
        assert expected_error in str(exc_info)

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
