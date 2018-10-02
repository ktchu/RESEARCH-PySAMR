"""
Unit tests for Geometry class

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
import copy

# External packages
import pytest

# XYZ
from samr.box import Box
from samr.geometry import Geometry


# --- NonAbstractGeometry

class NonAbstractGeometry(Geometry):
    """
    Concrete subclass of Geometry to use for testing purposes.
    """
    def compute_geometry(self, reference_box, box):
        """
        Return reference_geometry.
        """
        super().compute_geometry(reference_box, box)
        return copy.deepcopy(self)


# --- Tests

class GeometryTests:
    """
    Unit tests for Geometry class.
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(Geometry, 'num_dimensions')

    @staticmethod
    def test_init_1():
        """
        Test __init__(): valid parameters
        """
        # Exercise functionality
        num_dimensions = 3
        geometry = NonAbstractGeometry(num_dimensions)

        # Check results
        assert geometry.num_dimensions == num_dimensions

    @staticmethod
    def test_init_2():
        """
        Test __init__(): invalid 'num_dimensions'
        """
        # --- Exercise functionality and check results

        # num_dimensions not a numeric value
        with pytest.raises(ValueError) as exc_info:
            _ = NonAbstractGeometry(num_dimensions='not numeric')

        expected_error = "'num_dimensions' should be a numeric value"
        assert expected_error in str(exc_info)

        # num_dimensions not an integer value
        with pytest.raises(ValueError) as exc_info:
            _ = NonAbstractGeometry(num_dimensions=3.5)

        expected_error = "'num_dimensions' should be an integer"
        assert expected_error in str(exc_info)

        # num_dimensions = 0
        with pytest.raises(ValueError) as exc_info:
            _ = NonAbstractGeometry(num_dimensions=0)

        expected_error = "'num_dimensions' should be a positive number"
        assert expected_error in str(exc_info)

        # num_dimensions < 0
        with pytest.raises(ValueError) as exc_info:
            _ = NonAbstractGeometry(num_dimensions=-1)

        expected_error = "'num_dimensions' should be a positive number"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_repr():
        """
        Test __repr__().
        """
        # --- Preparations

        geometry = NonAbstractGeometry(3)

        # --- Exercise functionality and check results

        expected_repr = "Geometry(3)"
        assert repr(geometry) == expected_repr
        assert str(geometry) == expected_repr

    @staticmethod
    def test_compute_geometry():
        """
        Test compute_geometry(): invalid parametres
        """
        # --- Preparations

        num_dimensions = 3

        # Construct reference box and reference geometry
        reference_lower = [0] * num_dimensions
        reference_upper = [99] * num_dimensions
        reference_box = Box(reference_lower, reference_upper)

        reference_geometry = NonAbstractGeometry(num_dimensions)

        # Construct target box
        lower = [0] * num_dimensions
        upper = [199] * num_dimensions
        box = Box(lower, upper)

        # --- Exercise functionality and check results

        # 'reference_box' not a Box
        with pytest.raises(ValueError) as exc_info:
            _ = reference_geometry.compute_geometry(
                reference_box='not a Box', box=box)

        expected_error = "'reference_box' should be a Box"
        assert expected_error in str(exc_info)

        # 'box' not a Box
        with pytest.raises(ValueError) as exc_info:
            _ = reference_geometry.compute_geometry(
                reference_box=reference_box, box=[box])

        expected_error = "'box' should be a Box"
        assert expected_error in str(exc_info)

    @staticmethod
    def test_eq():
        """
        Test __eq__().
        """
        # --- Preparations

        num_dimensions = 100
        geometry = NonAbstractGeometry(num_dimensions)

        # --- Exercise functionality and check results

        # Two distinct NonAbstractGeometry objects that are equivalent
        equivalent_geometry = NonAbstractGeometry(num_dimensions)
        assert geometry == equivalent_geometry
        assert geometry is not equivalent_geometry

        # Two distinct NonAbstractGeometry objects that are not equivalent
        different_geometry = NonAbstractGeometry(num_dimensions + 1)
        assert geometry != different_geometry

        # Comparison with non-Geometry object
        assert geometry != 'not a NonAbstractGeometry object'
