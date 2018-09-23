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

# External packages
import numpy

# XYZ
from samr.geometry import Geometry
from .Box import Box
from .MeshBlock import MeshBlock
from .MeshLevel import MeshLevel


# --- Class definition

class Mesh:
    """
    TODO
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
        list: MeshLevels in Mesh
        """
        return self._levels

    @property
    def num_levels(self):
        """
        int: number of MeshLevels in Mesh
        """
        return len(self._levels)

    @property
    def blocks(self):
        """
        list: MeshBlocks in Mesh

        Notes
        -----
        * 'blocks' property is only available for single-level meshes
        """
        if not self.levels:
            raise RuntimeError("Mesh contains no blocks.")
        elif len(self.levels) > 1:
            raise RuntimeError("'blocks' is only available for "
                               "single-level meshes")

        return self.levels[0].blocks

    @property
    def num_blocks(self):
        """
        int: number of MeshBlocks in Mesh
        """
        return len(self.blocks)

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
        * When 'single_block' is set to True, 'single_level' is ignored.

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
        # TODO: implement compute_bounding_box()
        self._domain = copy.deepcopy(domain)
        self._bounding_box = self.domain[0]
        # self._bounding_box = Box.compute_bounding_box(domain)

        # geometry
        self._geometry = copy.deepcopy(geometry)

        # levels
        self._levels = []

        # --- Initialize levels for single-level meshes

        if single_block:
            # TODO
            block = MeshBlock(self.bounding_box, self.geometry)
            level = MeshLevel(block)
            self._levels.append(level)

        elif single_level:
            # TODO
            blocks = []
            for box in domain:
                block_geometry = None  # TODO
                blocks.append(MeshBlock(box, block_geometry))

            level = MeshLevel(blocks)
            self._levels.append(level)

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
