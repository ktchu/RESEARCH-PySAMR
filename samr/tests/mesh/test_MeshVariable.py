"""
Unit tests MeshVariable class

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
from samr import MeshVariable


# --- Tests

class MeshVariableTests(unittest.TestCase):
    """
    Unit tests for MeshVariable class.
    """
    # --- Test cases

    @staticmethod
    def test_attributes():
        """
        Test for expected attributes.
        """
        # Properties
        assert hasattr(MeshVariable, 'dtype')

    @staticmethod
    def test_init_1():
        """
        Test construction of MeshVariable object with default parameters.
        """
        # Exercise functionality
        mesh_variable = MeshVariable()

        # Check results
        assert mesh_variable.dtype == numpy.float64

    @staticmethod
    def test_init_2():
        """
        Test construction of MeshVariable object: precision='double'
        """
        # Exercise functionality
        mesh_variable = MeshVariable(precision='double')

        # Check results
        assert mesh_variable.dtype == numpy.float64

    @staticmethod
    def test_init_3():
        """
        Test construction of MeshVariable object: precision='single'
        """
        # Exercise functionality
        mesh_variable = MeshVariable(precision='single')

        # Check results
        assert mesh_variable.dtype == numpy.float32
