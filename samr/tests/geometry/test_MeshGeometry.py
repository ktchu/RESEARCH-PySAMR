"""
Unit tests MeshGeometry class

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

# XYZ
from samr.geometry import MeshGeometry


# --- Tests

class MeshGeometryTests(unittest.TestCase):
    """
    Unit tests for MeshGeometry class.
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(MeshGeometry, 'num_dimensions')
        assert hasattr(MeshGeometry, 'x_lower')
        assert hasattr(MeshGeometry, 'dx')

    @staticmethod
    def test_init_1():
        """
        Test construction of MeshGeometry object with default parameters.
        """
        # Exercise functionality
        num_dimensions = 3
        x_lower = numpy.array([0, 0, 0])
        dx = numpy.array([0, 0, 0])
        geometry = MeshGeometry(num_dimensions, x_lower, dx)

        # Check results
        assert geometry.num_dimensions == num_dimensions
        assert numpy.array_equal(geometry.x_lower, x_lower)
        assert geometry.x_lower.dtype == numpy.float64
        assert numpy.array_equal(geometry.dx, dx)
        assert geometry.dx.dtype == numpy.float64
