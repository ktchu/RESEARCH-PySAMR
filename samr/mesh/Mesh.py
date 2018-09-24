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
import copy

# XYZ
from samr.geometry import Geometry
from .Box import Box
from .MeshBlock import MeshBlock


# --- Class definition

class Mesh:
    """
    TODO

    * 'refinement level' = collection of MeshBlocks with the same level of
      refinement (relative to coarest level of Mesh)
    """
    # --- Properties

    @property
    def domain(self):
        """
        list: boxes that define the index space covered by Mesh on the
              coarsest level
        """
        return self._domain

    @property
    def bounding_box(self):
        """
        Box: smallest Box on coarsest level of mesh that covers domain
        """
        return self._bounding_box

    @property
    def geometry(self):
        """
        Geometry: geometry for Mesh on the coarsest level
        """
        return self._geometry

    @property
    def num_dimensions(self):
        """
        int: dimensionality of index space
        """
        return self.geometry.num_dimensions

    @property
    def levels(self):
        """
        list: refinement levels in Mesh
        """
        return self._levels

    @property
    def num_levels(self):
        """
        int: number of refinement levels in Mesh
        """
        return len(self._levels)

    @property
    def blocks(self, level_number=0):
        """
        list: MeshBlocks in Mesh
        """
        if level_number > self.num_levels:
            raise RuntimeError("'level_number' exceeds the number of levels "
                               "in Mesh")

        return self.levels[level_number]

    @property
    def num_blocks(self, level_number=0):
        """
        int: number of MeshBlocks in Mesh
        """
        if level_number > self.num_levels:
            raise RuntimeError("'level_number' exceeds the number of levels "
                               "in Mesh")

        return len(self.blocks)

    @property
    def data(self, variable, block_number=0):
        """
        TODO
        """
        # TODO
        pass

    @property
    def is_single_level(self):
        """
        boolean: True if Mesh is single-level; False otherwise
        """
        return self._is_single_level

    @property
    def is_single_block(self):
        """
        boolean: True if Mesh is single-block; False otherwise
        """
        return self._is_single_block

    # --- Public methods

    def __init__(self, domain, geometry,
                 single_level=False, single_block=False):
        """
        Initialize Mesh object.

        Parameters
        ----------
        domain: Box or list of Boxes
            list of boxes that define the index space covered by Mesh on the
            coarsest level

        geometry: Geometry
            geometry for Mesh on the coarsest level. Geometry parameters
            provided by 'geometry' apply to the bounding box for 'domain'.

        single_level: boolean
            True if Mesh will contain at most one level; False otherwise

        single_block: boolean
            True if Mesh will contain at most one block; False otherwise

        Notes
        -----
        * When 'single_block' is set to True, the Mesh.is_single_level is
          set to True. The value of the 'single_level' parameter is ignored.

        Examples
        --------
        TODO
        """
        # --- Check arguments

        # domain
        if not isinstance(domain, (Box, list, tuple)):
            raise ValueError("'domain' is not a Box object or a list of "
                             "Box objects")

        if isinstance(domain, (list, tuple)):
            for box in domain:
                if not isinstance(box, Box):
                    raise ValueError("'domain' contains a non-Box object")
        else:
            # Ensure that domain is a list
            domain = [domain]

        # geometry
        if not isinstance(geometry, Geometry):
            raise ValueError("'geometry' is not a Geometry object")

        # --- Set property and attribute values

        # index space
        self._domain = copy.deepcopy(domain)
        self._bounding_box = Box.compute_bounding_box(self.domain)

        # geometry
        self._geometry = copy.deepcopy(geometry)

        # refinement levels
        self._levels = []

        # is_single_block
        self._is_single_block = single_block

        # is_single_level
        if self.is_single_block:
            self._is_single_level = True
        else:
            self._is_single_level = single_level

        # --- Initialize levels for single-level meshes

        if single_block:
            block = MeshBlock(self.domain[0], self.geometry)
            level = [block]
            self._levels.append(level)

        else:
            level = []
            for box in domain:
                # TODO: fix computation of geometry for block
                block_geometry = self.geometry
                level.append(MeshBlock(box, block_geometry))

            self._levels.append(level)

    def add_level(self, level):
        """
        Add a refinement level to Mesh.

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
