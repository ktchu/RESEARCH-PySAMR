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
import enum
from enum import Enum

# External packages
import numpy

# XYZ
import samr
from .utils import array_is_empty
from .utils import contains_only_integers


# --- Class definition

class MeshVariable:
    """
    A MeshVariable object represents a mathematical variable on a Mesh. It
    defines the following properties of a mesh variable:

    * the location of variable values relative to mesh cells,

    * the width of stencil required to compute numerical quantities that
      depend on the variable,

    * the number of components that the variable has, and

    * the floating-point precision of variable values.
    """
    # --- Constants/Enumerations

    class Location(Enum):
        """
        Options for location of MeshVariable values on a mesh
        """
        CELL = enum.auto()
        NODE = enum.auto()
        FACE = enum.auto()

    class Precision(Enum):
        """
        Options for precision of MeshVariable data
        """
        DOUBLE = numpy.dtype(numpy.float64)
        SINGLE = numpy.dtype(numpy.float32)

    # --- Properties

    @property
    def mesh(self):
        """
        Mesh: mesh that MeshVariable is defined on
        """
        return self._mesh

    @property
    def location(self):
        """
        Location: location of values in mesh cell
        """
        return self._location

    @property
    def max_stencil_width(self):
        """
        numpy.ndarray: lower corner of index space covered by Box

        Notes
        -----
        * max_stencil_width.dtype = 'int64'
        """
        return self._max_stencil_width

    @property
    def depth(self):
        """
        int: number of components of MeshVariable
        """
        return self._depth

    @property
    def dtype(self):
        """
        numpy.dtype: data type of MeshVariable
        """
        return self._dtype

    # --- Public methods

    def __init__(self, mesh,
                 location=Location.NODE,
                 max_stencil_width=0,
                 depth=1,
                 precision=Precision.DOUBLE):
        """
        Initialize MeshVariable object.

        Parameters
        ----------
        mesh: Mesh object
            mesh that MeshVariable is defined on

        location: Location
            location of values in mesh cell

        max_stencil_width: int or list of ints
            maximum width of stencil applied to MeshVariable

        depth: int
            number of components of MeshVariable

        precision: Precision
            floating-point precision for MeshVariable

        Examples
        --------
        TODO
        """
        # pylint: disable=too-many-arguments

        # --- Check arguments

        # mesh
        if not isinstance(mesh, samr.mesh.Mesh):
            raise ValueError("'mesh' is not a Mesh object")

        # location
        if location not in MeshVariable.Location:
            raise ValueError("'location' not a valid Location value")

        # max_stencil_width has a valid type
        if not isinstance(max_stencil_width,
                          (int, float, list, tuple, numpy.ndarray)):
            raise ValueError("'max_stencil_width' is not a scalar, list, "
                             "tuple, or numpy.ndarray")

        if isinstance(max_stencil_width, (list, tuple, numpy.ndarray)):
            # max_stencil_width is not empty
            if array_is_empty(max_stencil_width):
                raise ValueError("'max_stencil_width' is empty")

            # max_stencil_width contains only integer values
            if not contains_only_integers(max_stencil_width):
                raise ValueError("'max_stencil_width' contains non-integer "
                                 "values")

        # depth
        if not isinstance(depth, (int, float)):
            raise ValueError("'depth' is not a numeric value")

        # depth is an integer value
        if depth % 1 != 0:
            raise ValueError("'depth' is not an integer")

        # precision
        if precision not in MeshVariable.Precision:
            raise ValueError("'precision' not a valid Precision value")

        # --- Initialize property and attribute values

        # mesh
        self._mesh = mesh

        # variable properties
        self._location = location

        if isinstance(max_stencil_width, (int, float)):
            max_stencil_width = [max_stencil_width] * mesh.num_dimensions

        self._max_stencil_width = numpy.array(max_stencil_width, dtype='int64')

        self._depth = depth
        self._dtype = precision.value

    def data(self, block_or_mesh):
        """
        Get data array for MeshVariable for specified MeshBlock.

        Parameters
        ----------
        block_or_mesh: MeshBlock or Mesh object
            MeshBlock or single-block Mesh to get data array from

        Return value
        ------------
        numpy.ndarray: data array from 'block' for MeshVariable

        Notes
        -----
        * When 'block_or_mesh' is a Mesh object, an error is raised if
          'block_or_mesh' is not a single-block Mesh (i.e.,
          Mesh.is_single_block is False).
        """
        # Case: 'block_or_mesh' is a MeshBlock
        if isinstance(block_or_mesh, samr.mesh.MeshBlock):

            # Retrieve and return data array
            return block_or_mesh.data(self)

        # Case: 'block_or_mesh' is a single-block Mesh object
        if isinstance(block_or_mesh, samr.mesh.Mesh):

            # Check arguments
            if not block_or_mesh.is_single_block:
                raise ValueError("'block_or_mesh' is not a single-block Mesh")

            # Retrieve and return data array
            return block_or_mesh.block.data(self)

        # Case: 'block_or_mesh' not a valid type
        raise ValueError("'block_or_mesh' is not a MeshBlock or Mesh "
                         "object")

    # --- Magic methods

    def __repr__(self):
        """
        Return unambiguous representation of object.

        Parameters
        ----------
        None

        Return value
        ------------
        str: unambiguous string representation of object

        Examples
        --------
        TODO
        """
        return "MeshVariable(mesh=<Mesh object at {}>, location={}, " \
               "max_stencil_width={}, depth={}, dtype={})". \
               format(hex(id(self.mesh)), self.location,
                      self.max_stencil_width, self.depth,
                      self.dtype.name)
