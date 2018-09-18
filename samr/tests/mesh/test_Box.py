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
        Test construction of Box object with valid parameters.
        """
        # Exercise functionality
        num_dimensions = 3
        lower = numpy.ones(num_dimensions)
        upper = 100 * numpy.ones(num_dimensions)
        box = Box(lower, upper)

        # Check results
        assert numpy.array_equal(box.lower, lower)
        assert box.lower.dtype == numpy.int64
        assert numpy.array_equal(box.upper, upper)
        assert box.upper.dtype == numpy.int64
        assert box.num_dimensions == num_dimensions
        assert numpy.array_equal(box.shape, numpy.array([100]*num_dimensions))
        assert box.size == numpy.product(box.shape)

    @staticmethod
    def test_init_2():
        """
        Test construction of Box object. Invalid 'lower'
        """
        # --- Preparations

        num_dimensions = 2
        upper = numpy.ones(num_dimensions)

        # --- Exercise functionality and check results

        # lower not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=3, upper=upper)

        if exc_info:
            expected_error = "'lower' is not a list, tuple, or numpy.ndarray"
        assert expected_error in str(exc_info)

        # lower contains non-integer values
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=numpy.array([0, 0.1, 0]), upper=upper)

        if exc_info:
            expected_error = "'lower' contains non-integer values"
        assert expected_error in str(exc_info)

        # len(lower) != len(upper)
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=numpy.zeros(num_dimensions-1), upper=upper)

        if exc_info:
            expected_error = "'lower' and 'upper' do not have the same " \
                             "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_3():
        """
        Test construction of Box object. Invalid 'upper'
        """
        # --- Preparations

        num_dimensions = 3
        lower = numpy.zeros(num_dimensions, dtype='int')

        # --- Exercise functionality and check results

        # upper not a valid array type
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower, upper='not a valid array type')

        if exc_info:
            expected_error = "'upper' is not a list, tuple, or numpy.ndarray"
        assert expected_error in str(exc_info)

        # upper contains non-integer values
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower, upper=numpy.array([0, 0.1, 0]))

        if exc_info:
            expected_error = "'upper' contains non-integer values"
        assert expected_error in str(exc_info)

        # len(lower) != len(upper)
        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower,
                    upper=numpy.ones(num_dimensions+1, dtype='int'))

        if exc_info:
            expected_error = "'lower' and 'upper' do not have the same " \
                             "number of components"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_init_4():
        """
        Test construction of Box object. Some componetns of 'upper' equal to
        components of 'lower'
        """
        # --- Preparations

        num_dimensions = 4
        lower = numpy.ones(num_dimensions, dtype='int')
        upper = 10 * numpy.ones(num_dimensions, dtype='int')
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
        Test construction of Box object. Component of 'upper' less than 'lower'
        """
        # --- Preparations

        num_dimensions = 5
        lower = numpy.ones(num_dimensions, dtype='int')
        upper = 10 * numpy.ones(num_dimensions, dtype='int')
        upper[1] = 0

        # --- Exercise functionality and check results

        with pytest.raises(ValueError) as exc_info:
            _ = Box(lower=lower, upper=upper)

        if exc_info:
            expected_error = \
                "Some components of 'upper' are less than components " \
                "of 'lower'"
        assert expected_error in str(exc_info)
