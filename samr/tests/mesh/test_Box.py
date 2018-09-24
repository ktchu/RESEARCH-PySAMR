"""
Unit tests for Box class

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
from samr.mesh import Box


# --- Tests

class BoxTests(unittest.TestCase):
    """
    Unit tests for Box class.
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(Box, 'lower')
        assert hasattr(Box, 'upper')
        assert hasattr(Box, 'num_dimensions')
        assert hasattr(Box, 'shape')
        assert hasattr(Box, 'size')

    @staticmethod
    def test_init_1():
        """
        Test __init__(): valid parameters
        """
        # --- Exercise functionality and check results

        # lower and upper are lists
        num_dimensions = 3
        lower = [1] * num_dimensions
        upper = [100] * num_dimensions
        box = Box(lower, upper)

        assert numpy.array_equal(box.lower, lower)
        assert box.lower.dtype == numpy.int64
        assert numpy.array_equal(box.upper, upper)
        assert box.upper.dtype == numpy.int64
        assert box.num_dimensions == num_dimensions
        assert numpy.array_equal(box.shape, [100] * num_dimensions)
        assert box.size == numpy.product(box.shape)

        # lower and upper are tuples
        num_dimensions = 3
        lower = tuple([1] * num_dimensions)
        upper = tuple([50] * num_dimensions)
        box = Box(lower, upper)

        assert numpy.array_equal(box.lower, lower)
        assert box.lower.dtype == numpy.int64
        assert numpy.array_equal(box.upper, upper)
        assert box.upper.dtype == numpy.int64
        assert box.num_dimensions == num_dimensions
        assert numpy.array_equal(box.shape, [50]*num_dimensions)
        assert box.size == numpy.product(box.shape)

        # lower and upper are numpy.ndarray objects
        num_dimensions = 3
        lower = numpy.ones(num_dimensions)
        upper = 20 * numpy.ones(num_dimensions)
        box = Box(lower, upper)

        assert numpy.array_equal(box.lower, lower)
        assert box.lower.dtype == numpy.int64
        assert numpy.array_equal(box.upper, upper)
        assert box.upper.dtype == numpy.int64
        assert box.num_dimensions == num_dimensions
        assert numpy.array_equal(box.shape, [20]*num_dimensions)
        assert box.size == numpy.product(box.shape)

    @staticmethod
    def test_init_2():
        """
        Test __init__(): invalid 'lower'
        """
        # --- Preparations

        num_dimensions = 2
        upper = [1] * num_dimensions

        # --- Exercise functionality and check results

        # lower not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=3, upper=upper)

        expected_error = "'lower' is not a list, tuple, or numpy.ndarray"
        assert expected_error in str(exc_info)

        # lower contains non-integer values
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=numpy.array([0, 0.1, 0]), upper=upper)

        expected_error = "'lower' contains non-integer values"
        assert expected_error in str(exc_info)

        # len(lower) != len(upper)
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=numpy.zeros(num_dimensions-1), upper=upper)

        expected_error = "'lower' and 'upper' do not have the same " \
                         "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_3():
        """
        Test __init__(): invalid 'upper'
        """
        # --- Preparations

        num_dimensions = 3
        lower = [0] * num_dimensions

        # --- Exercise functionality and check results

        # upper not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower, upper='not a valid array type')

        expected_error = "'upper' is not a list, tuple, or numpy.ndarray"
        assert expected_error in str(exc_info)

        # upper contains non-integer values
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower, upper=numpy.array([0, 0.1, 0]))

        expected_error = "'upper' contains non-integer values"
        assert expected_error in str(exc_info)

        # len(lower) != len(upper)
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower,
                    upper=numpy.ones(num_dimensions+1, dtype='int'))

        expected_error = "'lower' and 'upper' do not have the same " \
                         "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_4():
        """
        Test __init__(): some components of 'upper' equal to components of
        'lower'
        """
        # --- Preparations

        num_dimensions = 4
        lower = [0] * num_dimensions
        upper = [9.0] * num_dimensions
        upper[1] = lower[1]
        upper[-1] = lower[-1]

        # --- Exercise functionality and check results

        box = Box(lower, upper)
        assert numpy.array_equal(box.lower, lower)
        assert numpy.array_equal(box.upper, upper)
        assert box.num_dimensions == num_dimensions
        assert numpy.array_equal(box.shape, (10, 1, 10, 1))
        assert box.size == numpy.product(100)

    @staticmethod
    def test_init_5():
        """
        Test __init__(): component of 'upper' less than 'lower'
        """
        # --- Preparations

        num_dimensions = 5
        lower = [1] * num_dimensions
        upper = [10] * num_dimensions
        upper[1] = 0

        # --- Exercise functionality and check results

        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower, upper=upper)

        expected_error = "'upper' is less than 'lower' along some axes"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_compute_bounding_box_1():
        """
        Test compute_bounding_box(): normal usage
        """
        # --- Exercise functionality and check results

        # Test case 1
        boxes = [Box([0, 0], [9, 9]),
                 Box([10, 0], [19, 9]),
                 Box([20, 0], [29, 9])]

        expected_bounding_box = Box([0, 0], [29, 9])
        assert Box.compute_bounding_box(boxes) == expected_bounding_box

        # Test case 2
        boxes = [Box([0, 0], [9, 9]),
                 Box([10, 0], [19, 9]),
                 Box([20, 0], [29, 19])]

        expected_bounding_box = Box([0, 0], [29, 19])
        assert Box.compute_bounding_box(boxes) == expected_bounding_box

        # Test case 3
        boxes = [Box([0, 0], [9, 9]),
                 Box([10, 0], [19, 9]),
                 Box([-10, -10], [-1, 19])]

        expected_bounding_box = Box([-10, -10], [19, 19])
        assert Box.compute_bounding_box(boxes) == expected_bounding_box

        # Test case 4
        boxes = [Box([0, 0], [9, 9]),
                 Box([-10, -10], [19, 19])]

        expected_bounding_box = Box([-10, -10], [19, 19])
        assert Box.compute_bounding_box(boxes) == expected_bounding_box

    @staticmethod
    def test_compute_bounding_box_2():
        """
        Test compute_bounding_box(): invalid 'boxes'
        """
        # --- Exercise functionality and check results

        # 'boxes' is not list-like
        boxes = 'not a list'
        with pytest.raises(ValueError) as exc_info:
            _ = Box.compute_bounding_box(boxes)

        expected_error = "'boxes' is not a list of Box objects"
        assert expected_error in str(exc_info)

        # 'boxes' is not list-like
        boxes = (Box([0, 0], [9, 9]), 'not a Box')
        with pytest.raises(ValueError) as exc_info:
            _ = Box.compute_bounding_box(boxes)

        expected_error = "'boxes' contains a non-Box object"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_repr():
        """
        Test __repr__().
        """
        # --- Preparations

        num_dimensions = 4
        lower = [1] * num_dimensions
        upper = [10] * num_dimensions

        box = Box(lower, upper)

        # --- Exercise functionality and check results

        expected_repr = "Box([1, 1, 1, 1], [10, 10, 10, 10])"
        assert repr(box) == expected_repr
        assert str(box) == expected_repr

    @staticmethod
    def test_eq():
        """
        Test __eq__().
        """
        # --- Preparations

        num_dimensions = 4
        lower = [1] * num_dimensions
        upper = [10] * num_dimensions

        box = Box(lower, upper)

        # --- Exercise functionality and check results

        # Two distinct Box objects that are equivalent
        equivalent_box = Box(lower, upper)
        assert box == equivalent_box
        assert box is not equivalent_box

        # Two distinct Box objects that are not equivalent
        different_box = Box(lower, box.upper + [1, 2, 3, 4])
        assert box != different_box

        # Comparison with non-Box object
        assert box != 'not a Box object'

    @staticmethod
    def test_contains_only_integers():
        """
        Test contains_only_integers().
        """
        # pylint: disable=protected-access

        # --- Exercise functionality and check results

        # Normal usage
        assert Box._contains_only_integers([1, 2, 3])
        assert not Box._contains_only_integers([1, 2, 3.4])
        assert Box._contains_only_integers(1)
        assert not Box._contains_only_integers(1.5)

        # 'array' is not a scalar or array-like
        with pytest.raises(ValueError) as exc_info:
            Box._contains_only_integers('invalid array')

        expected_error = "'array' is not a scalar, list, tuple, or " \
                         "numpy.ndarray"
        assert expected_error in str(exc_info)

        # 'array' contains values that cannot be converted to a numeric value
        # 'array' cannot be converted to an array of numeric values
        with pytest.raises(ValueError) as exc_info:
            Box._contains_only_integers([1, 2, 2.5, 'non-numeric'])

        expected_error = "Unable to convert 'array' to an array of " \
                         "numeric values"
        assert expected_error in str(exc_info)
