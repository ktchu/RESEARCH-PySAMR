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
import enum
from enum import Enum

# External packages
import numpy

# XYZ
import samr
from samr.box import Box

from ..utils import array_is_empty
from ..utils import is_array
from ..utils import is_scalar
from ..utils import contains_only_integers


# --- Class definition

class MeshVariable:
    """
    A MeshVariable represents a mathematical variable on a Mesh. It defines
    the following properties of a mesh variable:

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
        NODE = enum.auto()
        CELL = enum.auto()
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
        numpy.ndarray: maximum number of mesh cells needed in each coordinate
            direction to apply stencil

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
        Initialize MeshVariable.

        Parameters
        ----------
        mesh: Mesh
            mesh that MeshVariable is defined on

        location: Location
            location of MeshVariable values in mesh cell

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

        # mesh has expected type
        if not isinstance(mesh, samr.mesh.Mesh):
            raise ValueError("'mesh' should be a Mesh")

        # location is a valid Location value
        if location not in MeshVariable.Location:
            raise ValueError("'location' is not a valid Location value")

        # check max_stencil_width parameter
        if is_array(max_stencil_width):

            # max_stencil_width is not empty
            if array_is_empty(max_stencil_width):
                raise ValueError("When 'max_stencil_width' is an array, "
                                 "it should not be empty")
            # max_stencil_width contains only integer values
            if not contains_only_integers(max_stencil_width):
                raise ValueError("When 'max_stencil_width' is an array, "
                                 "it should contain only integer values")

        elif not is_scalar(max_stencil_width):
            # max_stencil_width does not have a valid type
            raise ValueError("'max_stencil_width' should be a scalar or "
                             "non-string Sequence")

        # depth has expected type
        if not is_scalar(depth):
            raise ValueError("'depth' should be a numeric value")

        # depth is an integer value
        if depth % 1 != 0:
            raise ValueError("'depth' should be an integer")

        # precision is a valid Precision value
        if precision not in MeshVariable.Precision:
            raise ValueError("'precision' not a valid Precision value")

        # --- Initialize property and attribute values

        # mesh
        self._mesh = mesh

        # variable properties
        self._location = location

        if is_scalar(max_stencil_width):
            max_stencil_width = [max_stencil_width] * mesh.num_dimensions

        self._max_stencil_width = numpy.array(max_stencil_width, dtype='int64')

        self._depth = depth
        self._dtype = precision.value

    def data(self, block=None):
        """
        Get data array(s) for MeshVariable on specified MeshBlock.

        Parameters
        ----------
        block: MeshBlock
            MeshBlock to get data array from

        Return value
        ------------
        numpy.ndarray or list:
            data array(s) for MeshVariable on 'block'

        Notes
        -----
        * When 'block' is None, an error is raised if self.mesh is not
          a single-block Mesh (i.e., self.mesh.is_single_block is False).

        * When the depth of the MeshVariable is 1, the return value is an
          numpy.ndarray. When the depth of the MeshVariable is greater than
          1, the return value is a list of numpy.ndarray objects.
        """
        # --- Check arguments

        # block has expected type
        if block is not None:
            if not isinstance(block, samr.mesh.MeshBlock):
                raise ValueError("'block' should be a MeshBlock")

        elif not self.mesh.is_single_block:
            # self.mesh is a single-block Mesh
            raise ValueError("'block' is None, but self.mesh is a "
                             "multi-block Mesh. 'data' is only available "
                             "without specifying a 'block' when self.mesh "
                             "is a single-block Mesh.")

        # --- Retrieve and return data array

        if block:
            return block.data(self)

        return self.mesh.data(self)

    def data_shape(self, block=None):
        """
        Get shape of NumPy array for MeshVariable on specified MeshBlock.

        Parameters
        ----------
        block: MeshBlock
            MeshBlock to get shape of NumPy array for

        Return value
        ------------
        tuple: shape of numpy.ndarray for MeshVariable on 'block'

        Notes
        -----
        * When 'block' is None, an error is raised if self.mesh is not
          a single-block Mesh (i.e., self.mesh.is_single_block is False).
        """
        # Compute shape of box for MeshVariable with halo on 'block'
        shape = self.box(block, with_halo=True).shape

        # Adjust shape for location of MeshVariable
        if self.location == MeshVariable.Location.NODE:
            shape += 1

        elif self.location == MeshVariable.Location.FACE:
            # TODO: figure out how to represent this
            pass

        # Adjust shape for depth
        # TODO: add parameter to use first index for MeshVariable components
        if self.location in \
                [MeshVariable.Location.CELL, MeshVariable.Location.NODE] and \
                self.depth > 1:
            shape = numpy.array(list(shape) + [self.depth])

        return shape

    def box(self, block=None, with_halo=False):
        """
        Get box for MeshVariable on specified MeshBlock.

        Parameters
        ----------
        block: MeshBlock
            MeshBlock to get box for

        with_halo: bool
            True if box should include halo cells; False otherwise

        Return value
        ------------
        Box: box for MeshVariable on 'block'

        Notes
        -----
        * When 'block' is None, an error is raised if self.mesh is not
          a single-block Mesh (i.e., self.mesh.is_single_block is False).
        """
        # --- Check arguments

        # block has expected type
        if block is not None:
            if not isinstance(block, samr.mesh.MeshBlock):
                raise ValueError("'block' should be a MeshBlock")

        elif not self.mesh.is_single_block:
            # self.mesh is a single-block Mesh
            raise ValueError("'block' is None, but self.mesh is a "
                             "multi-block Mesh. 'data' is only available "
                             "without specifying a 'block' when self.mesh "
                             "is a single-block Mesh.")

        # --- Compute box for MeshVariable

        if block:
            if with_halo:
                box = Box(block.lower - self.max_stencil_width,
                          block.upper + self.max_stencil_width)
            else:
                box = copy.deepcopy(block.box)

        else:
            if with_halo:
                box = Box(self.mesh.domain.lower - self.max_stencil_width,
                          self.mesh.domain.upper + self.max_stencil_width)
            else:
                box = copy.deepcopy(self.mesh.domain)

        return box

    def geometry(self, block=None):
        """
        Get geometry for MeshVariable on specified MeshBlock.

        Parameters
        ----------
        block: MeshBlock
            MeshBlock to get box for

        Return value
        ------------
        Geometry: geometry for MeshVariable on 'block'

        Notes
        -----
        * When 'block' is None, an error is raised if self.mesh is not
          a single-block Mesh (i.e., self.mesh.is_single_block is False).
        """
        # --- Check arguments

        # block has expected type
        if block is not None:
            if not isinstance(block, samr.mesh.MeshBlock):
                raise ValueError("'block' should be a MeshBlock")

        elif not self.mesh.is_single_block:
            # self.mesh is a single-block Mesh
            raise ValueError("'block' is None, but self.mesh is a "
                             "multi-block Mesh. 'data' is only available "
                             "without specifying a 'block' when self.mesh "
                             "is a single-block Mesh.")

        # --- Retrieve and return data array

        if block:
            return block.geometry

        return self.mesh.geometry

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
