"""
Unit tests for MeshVariable class

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
from samr.mesh import MeshVariable


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
        assert hasattr(MeshVariable, 'mesh')
        assert hasattr(MeshVariable, 'location')
        assert hasattr(MeshVariable, 'max_stencil_width')
        assert hasattr(MeshVariable, 'depth')
        assert hasattr(MeshVariable, 'dtype')

    @unittest.skip('')
    @staticmethod
    def test_init_1():
        """
        Test construction of MeshVariable with default parameters.
        """
        # Exercise functionality
        mesh_variable = MeshVariable()

        # Check results
        assert mesh_variable.dtype == numpy.float64

    @unittest.skip('')
    @staticmethod
    def test_init_2():
        """
        Test construction of MeshVariable: precision='double'
        """
        # Exercise functionality
        mesh_variable = MeshVariable(precision='double')

        # Check results
        assert mesh_variable.dtype == numpy.float64

    @unittest.skip('')
    @staticmethod
    def test_init_3():
        """
        Test construction of MeshVariable: precision='single'
        """
        # Exercise functionality
        mesh_variable = MeshVariable(precision='single')

        # Check results
        assert mesh_variable.dtype == numpy.float32
