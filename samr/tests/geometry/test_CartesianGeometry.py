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
from samr.box import Box
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
        assert hasattr(CartesianGeometry, 'x_upper')
        assert hasattr(CartesianGeometry, 'shape')

    @staticmethod
    def test_init_1():
        """
        Test __init__(): valid parameters
        """
        # --- Exercise functionality and check results

        # x_lower and x_upper are lists
        num_dimensions = 3
        x_lower = [0] * num_dimensions
        x_upper = [0.1] * num_dimensions
        geometry = CartesianGeometry(x_lower, x_upper)

        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.x_upper, x_upper)
        assert geometry.x_upper.dtype == numpy.float64

        expected_shape = numpy.array(x_upper) - numpy.array(x_lower)
        assert numpy.array_equal(geometry.shape, expected_shape)
        assert geometry.shape.dtype == numpy.float64

        # x_lower and x_upper are tuples
        num_dimensions = 3
        x_lower = tuple([0] * num_dimensions)
        x_upper = tuple([0.1] * num_dimensions)
        geometry = CartesianGeometry(x_lower, x_upper)

        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.x_upper, x_upper)
        assert geometry.x_upper.dtype == numpy.float64

        expected_shape = numpy.array(x_upper) - numpy.array(x_lower)
        assert numpy.array_equal(geometry.shape, expected_shape)
        assert geometry.shape.dtype == numpy.float64

        # x_lower and x_upper are numpy.ndarray objects
        num_dimensions = 3
        x_lower = numpy.zeros(num_dimensions)
        x_upper = 0.1 * numpy.ones(num_dimensions)
        geometry = CartesianGeometry(x_lower, x_upper)

        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.x_upper, x_upper)
        assert geometry.x_upper.dtype == numpy.float64

        expected_shape = numpy.array(x_upper) - numpy.array(x_lower)
        assert numpy.array_equal(geometry.shape, expected_shape)
        assert geometry.shape.dtype == numpy.float64

    @staticmethod
    def test_init_2():
        """
        Test __init__(): invalid 'x_lower'
        """
        # --- Preparations

        num_dimensions = 5
        x_upper = [0.1] * num_dimensions

        # --- Exercise functionality and check results

        # x_lower not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=3, x_upper=x_upper)

        expected_error = "'x_lower' should be list-like or a numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(x_lower) != len(x_upper)
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=[0] * (num_dimensions-1),
                                  x_upper=x_upper)

        expected_error = "'x_lower' and 'x_upper' should have the same " \
                         "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_3():
        """
        Test __init__(): invalid 'x_upper'
        """
        # --- Preparations

        num_dimensions = 5
        x_lower = [0] * num_dimensions

        # --- Exercise functionality and check results

        # x_upper not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=x_lower,
                                  x_upper='not a numpy.ndarray')

        expected_error = "'x_upper' should be list-like or a numpy.ndarray"
        assert expected_error in str(exc_info)

        # len(x_lower) != len(x_upper)
        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=x_lower,
                                  x_upper=[1.0] * (num_dimensions+1))

        expected_error = "'x_lower' and 'x_upper' should have the same " \
                         "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_4():
        """
        Test __init__(): 'x_upper' less than or equal to 'x_lower' along some
        axes
        """
        # --- Exercise functionality and check results

        # 'x_upper' less than 'x_lower' along some axes
        num_dimensions = 5
        x_lower = [0] * num_dimensions
        x_upper = [10] * num_dimensions
        x_upper[1] = -1

        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=x_lower, x_upper=x_upper)

        expected_error = "'x_upper' should be greater than 'x_lower' along " \
                         "all axes"
        assert expected_error in str(exc_info)

        # 'x_upper' equal to than 'x_lower' along some axes
        num_dimensions = 10
        x_lower = [0] * num_dimensions
        x_upper = [10] * num_dimensions
        x_upper[0] = 0.0
        x_upper[-1] = 0.0

        with pytest.raises(ValueError) as exc_info:
            _ = CartesianGeometry(x_lower=x_lower, x_upper=x_upper)

        expected_error = "'x_upper' should be greater than 'x_lower' along " \
                         "all axes"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_compute_geometry_1():
        """
        Test compute_geometry(): normal usage
        """
        # --- Preparations

        num_dimensions = 3

        # Construct reference box and reference geometry
        reference_lower = [0] * num_dimensions
        reference_upper = [99] * num_dimensions
        reference_box = Box(reference_lower, reference_upper)

        reference_x_lower = [-1] * num_dimensions
        reference_x_upper = [1] * num_dimensions

        reference_geometry = CartesianGeometry(reference_x_lower,
                                               reference_x_upper)

        # Construct target box
        lower = [0] * num_dimensions
        upper = [199] * num_dimensions
        box = Box(lower, upper)

        # --- Exercise functionality and check results

        geometry = reference_geometry.compute_geometry(reference_box, box)

        assert numpy.array_equal(geometry.x_lower, reference_geometry.x_lower)
        assert numpy.array_equal(geometry.x_upper, [3] * num_dimensions)

    @staticmethod
    def test_compute_geometry_2():
        """
        Test compute_geometry(): invalid parameters
        """
        # --- Preparations

        num_dimensions = 3

        # Construct reference box and reference geometry
        reference_lower = [0] * num_dimensions
        reference_upper = [99] * num_dimensions
        reference_box = Box(reference_lower, reference_upper)

        reference_x_lower = [-1] * num_dimensions
        reference_x_upper = [1] * num_dimensions

        reference_geometry = CartesianGeometry(reference_x_lower,
                                               reference_x_upper)

        # Construct target box
        lower = [0] * num_dimensions
        upper = [199] * num_dimensions
        box = Box(lower, upper)

        # --- Exercise functionality and check results

        # box not a Box
        with pytest.raises(ValueError) as exc_info:
            _ = reference_geometry.compute_geometry(
                reference_box=reference_box, box='not a Box')

        expected_error = "'box' should be a Box"
        assert expected_error in str(exc_info)

        # reference_box not a Box
        with pytest.raises(ValueError) as exc_info:
            _ = reference_geometry.compute_geometry(
                reference_box=numpy.array([[0, 0], [9, 9]]), box=box)

        expected_error = "'reference_box' should be a Box"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_compute_dx():
        """
        Test compute_dx().
        """
        # --- Preparations

        num_dimensions = 3
        x_lower = [-1] * num_dimensions
        x_upper = [1] * num_dimensions

        geometry = CartesianGeometry(x_lower, x_upper)

        lower = [0] * num_dimensions
        upper = [99] * num_dimensions
        box = Box(lower, upper)

        # --- Exercise functionality and check results

        dx = geometry.compute_dx(box)
        expected_dx = [0.02] * num_dimensions
        assert numpy.array_equal(dx, expected_dx)

    @staticmethod
    def test_repr():
        """
        Test __repr__().
        """
        # --- Preparations

        num_dimensions = 3
        x_lower = [0] * num_dimensions
        x_upper = [1] * num_dimensions

        geometry = CartesianGeometry(x_lower, x_upper)

        # --- Exercise functionality and check results

        expected_repr = "CartesianGeometry([0.0, 0.0, 0.0], [1.0, 1.0, 1.0])"
        assert repr(geometry) == expected_repr
        assert str(geometry) == expected_repr

    @staticmethod
    def test_eq():
        """
        Test __eq__().
        """
        # --- Preparations

        num_dimensions = 3
        x_lower = [0] * num_dimensions
        x_upper = [1] * num_dimensions

        geometry = CartesianGeometry(x_lower, x_upper)

        # --- Exercise functionality and check results

        # Two distinct CartesianGeometry objects that are equivalent
        equivalent_geometry = CartesianGeometry(x_lower, x_upper)
        assert geometry == equivalent_geometry
        assert geometry is not equivalent_geometry

        # Two distinct CartesianGeometry objects that are not equivalent
        different_geometry = CartesianGeometry(geometry.x_lower - 1, x_upper)
        assert geometry != different_geometry

        # Comparison with non-CartesianGeometry object
        assert geometry != 'not a CartesianGeometry object'
