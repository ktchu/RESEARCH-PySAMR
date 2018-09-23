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
        Test __init__(): valid parameters
        """
        # --- Exercise functionality and check results

        # x_lower and dx are lists
        num_dimensions = 3
        x_lower = [0] * num_dimensions
        dx = [0.1] * num_dimensions
        geometry = CartesianGeometry(x_lower, dx)

        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.dx, dx)
        assert geometry.dx.dtype == numpy.float64

        # x_lower and dx are tuples
        num_dimensions = 3
        x_lower = tuple([0] * num_dimensions)
        dx = tuple([0.1] * num_dimensions)
        geometry = CartesianGeometry(x_lower, dx)

        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.dx, dx)
        assert geometry.dx.dtype == numpy.float64

        # x_lower and dx are numpy.ndarray objects
        num_dimensions = 3
        x_lower = numpy.zeros(num_dimensions)
        dx = 0.1 * numpy.ones(num_dimensions)
        geometry = CartesianGeometry(x_lower, dx)

        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.dx, dx)
        assert geometry.dx.dtype == numpy.float64

    @staticmethod
    def test_init_2():
        """
        Test __init__(): invalid 'x_lower'
        """
        # --- Preparations

        num_dimensions = 5
        dx = [0.1] * num_dimensions

        # --- Exercise functionality and check results

        # x_lower not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=3, dx=dx)

        expected_error = "'x_lower' is not a list, tuple, or numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(x_lower) != len(dx)
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=[0] * (num_dimensions-1), dx=dx)

        expected_error = "'x_lower' and 'dx' do not have the same " \
                         "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_3():
        """
        Test __init__(): invalid 'x_lower'
        """
        # --- Preparations

        num_dimensions = 5
        x_lower = [0] * num_dimensions

        # --- Exercise functionality and check results

        # dx not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=x_lower, dx='not a numpy.ndarray')

        expected_error = "'dx' is not a list, tuple, or numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(x_lower) != len(dx)
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=x_lower,
                                  dx=[0.1] * (num_dimensions+1))

        expected_error = "'x_lower' and 'dx' do not have the same " \
                         "number of components"
        assert expected_error in str(exc_info)

        # dx contains a zero value
        with pytest.raises(ValueError) as exc_info:
            invalid_dx = [0.1] * num_dimensions
            invalid_dx[0] = 0
            _ = CartesianGeometry(x_lower=x_lower, dx=invalid_dx)

        expected_error = "'dx' contains a non-positive value"
        assert expected_error in str(exc_info)

        # dx contains a negative value
        with pytest.raises(ValueError) as exc_info:
            invalid_dx = [0.1] * num_dimensions
            invalid_dx[-1] = -0.1
            _ = CartesianGeometry(x_lower=x_lower, dx=invalid_dx)

        expected_error = "'dx' contains a non-positive value"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_eq():
        """
        Test __eq__().
        """
        # --- Preparations

        num_dimensions = 3
        x_lower = [0] * num_dimensions
        dx = [0.1] * num_dimensions

        geometry = CartesianGeometry(x_lower, dx)

        # --- Exercise functionality and check results

        # Two distinct CartesianGeometry objects that are equivalent
        equivalent_geometry = CartesianGeometry(x_lower, dx)
        assert geometry == equivalent_geometry
        assert geometry is not equivalent_geometry

        # Two distinct CartesianGeometry objects that are not equivalent
        different_geometry = CartesianGeometry(geometry.x_lower + 1, dx)
        assert geometry != different_geometry

        # Comparison with non-CartesianGeometry object
        assert geometry != 'not a CartesianGeometry object'
