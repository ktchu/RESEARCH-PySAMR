"""
TODO: add docstring

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

# External packages
import numpy

# XYZ
from samr.geometry import Geometry
from .MeshBlock import MeshBlock
from .MeshLevel import MeshLevel


# --- Constants

# numpy integer data types
from .constants import NUMPY_INT_DTYPES


# --- Class definition

class Mesh:
    """
    TODO
    """
    # --- Properties

    @property
    def num_dimensions(self):
        """
        int: dimensionality of index space
        """
        return self.geometry.num_dimensions

    @property
    def geometry(self):
        """
        Geometry: geometry for coarsest level of mesh
        """
        return self._geometry

    @property
    def domain(self):
        """
        MeshLevel: union of blocks on coarsest level of mesh
        """
        if not self.levels:
            return None

        return self.levels[0]

    @property
    def domain_block(self):
        """
        MeshBlock: block on coarsest level of mesh that covers domain
        """
        return self._domain_block

    @property
    def levels(self):
        """
        list: MeshLevels in Mesh
        """
        return self._levels

    @property
    def blocks(self):
        """
        list: MeshBlocks in Mesh
        """
        if not self.levels:
            raise RuntimeError("Mesh contains no blocks.")
        elif len(self.levels) > 1:
            raise RuntimeError("'blocks' is unavailable when for "
                               "multi-level meshes")

        return self.levels[0].blocks

    # --- Public methods

    def __init__(self, geometry, lower, upper,
                 single_level=False, single_block=False):
        """
        TODO

        Parameters
        ----------
        geometry: Geometry
            geometry for coarsest level of mesh

        lower: numpy.ndarray of integers
            lower corner of index space for coarsest level of mesh

        upper: numpy.ndarray of integers
            upper corner of index space for coarsest level of mesh

        single_level: boolean
            True if Mesh will contain at most one level; False otherwise

        single_block: boolean
            True if Mesh will contain at most one block; False otherwise

        Examples
        --------
        TODO
        """
        # TODO
        # - consider replacing (lower, upper) parameters with
        #   domain_boxes = list of (lower, upper) tuples.
        #
        # - add validation of domain boxes

        # --- Check arguments

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' is not Geometry object")

        # get dimensionality of geometry
        num_dimensions = geometry.num_dimensions

        # lower
        if not isinstance(lower, numpy.ndarray):
            raise ValueError("'lower' is not a numpy.ndarray")

        if len(lower) != num_dimensions:
            err_msg = "'lower' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        if lower.dtype not in NUMPY_INT_DTYPES:
            err_msg = "'lower' does not have an integer dtype"
            raise ValueError(err_msg)

        # upper
        if not isinstance(upper, numpy.ndarray):
            raise ValueError("'upper' is not a numpy.ndarray")

        if len(upper) != num_dimensions:
            err_msg = "'upper' does not have 'num_dimensions' components"
            raise ValueError(err_msg)

        if upper.dtype not in NUMPY_INT_DTYPES:
            err_msg = "'upper' does not have an integer dtype"
            raise ValueError(err_msg)

        # upper > lower
        if not numpy.all(numpy.greater(upper, lower)):
            err_msg = "Some components of 'upper' are less than or equal " \
                      "to components of 'lower'"
            raise ValueError(err_msg)

        # --- Set property and attribute values

        # PYLINT: eliminate 'defined outside __init__' error
        self._data = {}

        # index space
        self._lower = lower.astype('int64')
        self._upper = upper.astype('int64')

        # geometry
        self._geometry = geometry

        # --- Set property and attribute values

        # PYLINT: eliminate 'defined outside __init__' error
        self._levels = []

        self._geometry = geometry
        self._domain_block = MeshBlock(geometry, lower, upper)

        # --- Initialize domain and levels for single-level meshes

        # TODO

    def add_level(self, mesh_level):
        """
        Add a MeshLevel to Mesh.

        Parameters
        ----------
        TODO

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # TODO
        pass
