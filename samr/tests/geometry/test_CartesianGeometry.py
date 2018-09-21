"""
Unit tests for CartesianGeometry class

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


# --- Tests

class CartesianGeometryTests(unittest.TestCase):
    """
    Unit tests for CartesianGeometry class.
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(CartesianGeometry, 'num_dimensions')
        assert hasattr(CartesianGeometry, 'x_lower')
        assert hasattr(CartesianGeometry, 'dx')

    @staticmethod
    def test_init_1():
        """
        Test construction of CartesianGeometry object with valid parameters.
        """
        # Exercise functionality
        num_dimensions = 3
        x_lower = numpy.zeros(num_dimensions)
        dx = 0.1 * numpy.ones(num_dimensions)
        geometry = CartesianGeometry(num_dimensions, x_lower, dx)

        # Check results
        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.dx, dx)
        assert geometry.dx.dtype == numpy.float64

    @staticmethod
    def test_init_2():
        """
        Test construction of CartesianGeometry object. Invalid 'num_dimensions'
        """
        # --- Preparations

        num_dimensions = 5
        x_lower = numpy.zeros(num_dimensions)
        dx = 0.1 * numpy.ones(num_dimensions)

        # --- Exercise functionality and check results

        # num_dimensions not an int
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions='not an int',
                                  x_lower=x_lower,
                                  dx=dx)

        if exc_info:
            expected_error = "'num_dimensions' is not an integer"
        assert expected_error in str(exc_info)

        # num_dimensions = 0
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions=0,
                                  x_lower=x_lower,
                                  dx=dx)

        if exc_info:
            expected_error = "'num_dimensions' is not a positive value"
        assert expected_error in str(exc_info)

        # num_dimensions < 0
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions=-1,
                                  x_lower=x_lower,
                                  dx=dx)

        if exc_info:
            expected_error = "'num_dimensions' is not a positive value"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_3():
        """
        Test construction of CartesianGeometry object. Invalid 'x_lower'
        """
        # --- Preparations

        num_dimensions = 5
        dx = 0.1 * numpy.ones(num_dimensions)

        # --- Exercise functionality and check results

        # x_lower not a numpy.ndarray
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions=num_dimensions,
                                  x_lower=3,
                                  dx=dx)

        if exc_info:
            expected_error = "'x_lower' is not a numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(x_lower) != num_dimensions
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions=num_dimensions,
                                  x_lower=numpy.zeros(num_dimensions-1),
                                  dx=dx)

        if exc_info:
            expected_error = "'x_lower' does not have 'num_dimensions' " \
                             "components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_4():
        """
        Test construction of CartesianGeometry object. Invalid 'x_lower'
        """
        # --- Preparations

        num_dimensions = 5
        x_lower = numpy.zeros(num_dimensions)

        # --- Exercise functionality and check results

        # dx not a numpy.ndarray
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions=num_dimensions,
                                  x_lower=x_lower,
                                  dx='not a numpy.ndarray')

        if exc_info:
            expected_error = "'dx' is not a numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(dx) != num_dimensions
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(num_dimensions=num_dimensions,
                                  x_lower=x_lower,
                                  dx=numpy.ones(num_dimensions+1))

        if exc_info:
            expected_error = "'dx' does not have 'num_dimensions' " \
                             "components"
        assert expected_error in str(exc_info)

        # dx contains a zero value
        with pytest.raises(ValueError) as exc_info:
            invalid_dx = numpy.ones(num_dimensions)
            invalid_dx[0] = 0
            _ = CartesianGeometry(num_dimensions=num_dimensions,
                                  x_lower=x_lower,
                                  dx=invalid_dx)

        if exc_info:
            expected_error = "'dx' contains a non-positive value"
        assert expected_error in str(exc_info)

        # dx contains a negative value
        with pytest.raises(ValueError) as exc_info:
            invalid_dx = numpy.ones(num_dimensions)
            invalid_dx[-1] = -0.1
            _ = CartesianGeometry(num_dimensions=num_dimensions,
                                  x_lower=x_lower,
                                  dx=invalid_dx)

        if exc_info:
            expected_error = "'dx' contains a non-positive value"
        assert expected_error in str(exc_info)
