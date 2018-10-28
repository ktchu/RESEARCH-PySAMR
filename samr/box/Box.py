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
from ..utils import array_is_empty
from ..utils import contains_only_integers
from ..utils import is_array
from ..utils import is_scalar


# --- Class definition

class Box:
    """
    A Box represents a rectangular region of index space.
    """
    # --- Properties

    @property
    def lower(self):
        """
        numpy.ndarray: lower corner of index space covered by Box

        Notes
        -----
        * lower.dtype = 'int64'
        """
        return self._lower

    @property
    def upper(self):
        """
        numpy.ndarray: upper corner of index space covered by Box

        Notes
        -----
        * upper.dtype = 'int64'
        """
        return self._upper

    @property
    def num_dimensions(self):
        """
        int: dimensionality of Box
        """
        return self._num_dimensions

    @property
    def shape(self):
        """
        numpy.ndarray: number of cells Box has in each coordinate direction

        Notes
        -----
        * upper.dtype = 'int64'
        """
        return self._shape

    @property
    def size(self):
        """
        int: number of cells in Box
        """
        return self._size

    # --- Public methods

    def __init__(self, lower, upper):
        """
        Initialize Box.

        Parameters
        ----------
        lower: list-like (e.g., list, tuple) or numpy.ndarray
            lower corner of index space covered by Box

        upper: list-like (e.g., list, tuple) or numpy.ndarray
            upper corner of index space covered by Box

        Examples
        --------
        >>> lower = [0, 0, 0]
        >>> upper = [9, 9, 9]
        >>> box = Box(lower, upper)
        >>> box.num_dimensions
        3
        >>> box.shape
        array([10, 10, 10])
        >>> box.size
        1000
        """
        # --- Check arguments

        # lower has expected_type
        if not is_array(lower):
            raise ValueError("'lower' should be list-like or a numpy.ndarray")

        # lower is not empty
        if array_is_empty(lower):
            raise ValueError("'lower' should not be empty")

        # lower contains only integer values
        if not contains_only_integers(lower):
            raise ValueError("'lower' should contain only integer values")

        # upper has expected_type
        if not is_array(upper):
            raise ValueError("'upper' should be list-like or a numpy.ndarray")

        # upper is not empty
        if array_is_empty(upper):
            raise ValueError("'upper' should not be empty")

        # upper contains only integer values
        if not contains_only_integers(upper):
            raise ValueError("'upper' should contain only integer values")

        # len(lower) == len(upper)
        if len(lower) != len(upper):
            raise ValueError("'lower' and 'upper' should have the same number "
                             "of components")

        # upper >= lower
        if not numpy.all(numpy.greater_equal(upper, lower)):
            raise ValueError("'upper' should be greater than or equal to "
                             "'lower' along all axes")

        # --- Initialize property and attribute values

        # index space
        self._lower = numpy.array(lower, dtype='int64')
        self._upper = numpy.array(upper, dtype='int64')

        # num_dimensions
        self._num_dimensions = len(self.lower)

        # shape
        self._shape = self.upper - self.lower + \
            numpy.ones(self.num_dimensions, dtype='int64')

        # size
        self._size = numpy.product(self.shape)

    # --- Public static methods

    @staticmethod
    def compute_bounding_box(boxes):
        """
        Compute bounding box for list of boxes.

        Parameters
        ----------
        boxes: list of Boxes or Box
            boxes to compute bounding box for

        Return value
        ------------
        Box: bounding box

        Examples
        --------
        >>> boxes = [Box([0, 0, 0], [2, 2, 2]), Box([-2, -2, 0], [1, 1, 3])]
        >>> Box.compute_bounding_box(boxes)
        Box([-2, -2, 0], [2, 2, 3])

        >>> box = Box([0, 0], [9, 9])
        >>> Box.compute_bounding_box(box)
        Box([0, 0], [9, 9])
        """
        # --- Check arguments

        # boxes has expected type
        if is_array(boxes, exclude_numpy_ndarray=True):
            # boxes contains only Box items
            for box in boxes:
                if not isinstance(box, Box):
                    raise ValueError("'boxes' should not contain non-Box "
                                     "items")

        elif isinstance(boxes, Box):
            # ensure that boxes is list-like
            boxes = [boxes]

        else:
            raise ValueError("'boxes' should be a list of Boxes or a Box")

        # --- Compute bounding box

        bounding_box_lower = numpy.min([box.lower for box in boxes], axis=0)
        bounding_box_upper = numpy.max([box.upper for box in boxes], axis=0)

        return Box(bounding_box_lower, bounding_box_upper)

    @staticmethod
    def refine_boxes(boxes, factor):
        """
        Refine boxes by specified factor.

        Parameters
        ----------
        boxes: Box or list of Boxes
            boxes to refine

        factor: int, list-like (e.g., list, tuple), or numpy.ndarray
            factor to refine boxes by in each coordinate direction

        Return value
        ------------
        list of Boxes: list of refined boxes

        Examples
        --------
        >>> boxes = [Box([0, 0], [9, 9]), Box([0, 10], [9, 19])]
        >>> Box.refine_boxes(boxes, [3, 2])
        [Box([0, 0], [29, 19]), Box([0, 20], [29, 39])]

        >>> Box.refine_boxes(Box([0, 0], [4, 4]), 4)
        [Box([0, 0], [19, 19])]
        """
        # pylint: disable=too-many-branches

        # --- Check arguments

        # check boxes parameter
        if isinstance(boxes, Box):

            # ensure that boxes is a list
            boxes = [boxes]

        elif not is_array(boxes, exclude_numpy_ndarray=True):
            # boxes does not have a valid type
            raise ValueError("'boxes' should be a Box or list of Boxes")

        # boxes contains only Box items
        for box in boxes:
            if not isinstance(box, Box):
                raise ValueError("'boxes' should not contain non-Box items")

        # boxes all have the same dimensionality
        num_dimensions = boxes[0].num_dimensions
        for box in boxes[1:]:
            if box.num_dimensions != num_dimensions:
                raise ValueError("All Box objects in 'boxes' should have "
                                 "the same 'num_dimensions' value")

        # check factor parameter
        if is_scalar(factor):
            # factor is an integer value
            if factor % 1 != 0:
                raise ValueError("When 'factor' is a scalar, it should be an "
                                 "integer")

        elif is_array(factor):
            # factor is not empty
            if array_is_empty(factor):
                raise ValueError("When 'factor' is an array, it should not "
                                 "be empty")

            # factor contains only integer values
            if not contains_only_integers(factor):
                raise ValueError("When 'factor' is an array, it should "
                                 "contain only integer values")

            # len(factor) == num_dimensions
            if len(factor) != num_dimensions:
                raise ValueError("When 'factor' is an array, its length "
                                 "should be equal to the dimensionality of "
                                 "the Box items in 'boxes'")
        else:
            # factor does not have a valid type
            raise ValueError("'factor' should be an int, list-like, or a "
                             "numpy.ndarray")

        # --- Preparations

        # Convert factor to numpy.ndarray
        factor = factor * numpy.ones(num_dimensions, dtype='int')

        # --- Refine boxes

        refined_boxes = []
        for box in boxes:
            refined_boxes.append(Box(box.lower * factor,
                                     (box.upper + 1) * factor - 1))

        return refined_boxes

    @staticmethod
    def coarsen_boxes(boxes, factor):
        """
        Coarsen boxes by specified factor.

        Parameters
        ----------
        boxes: list of Boxes
            boxes to coarsen

        factor: int, list-like (e.g., list, tuple), or numpy.ndarray
            factor to coarsen boxes by in each coordinate direction

        Return value
        ------------
        list of Boxes: list of coarsened boxes

        Examples
        --------
        >>> boxes = [Box([0, 0], [9, 9]), Box([0, 10], [9, 19])]
        >>> Box.coarsen_boxes(boxes, [3, 2])
        [Box([0, 0], [3, 4]), Box([0, 5], [3, 9])]

        >>> Box.coarsen_boxes(Box([0, 0], [19, 19]), 4)
        [Box([0, 0], [4, 4])]
        """
        # pylint: disable=too-many-branches

        # --- Check arguments

        # check boxes parameter
        if isinstance(boxes, Box):

            # ensure that boxes is a list
            boxes = [boxes]

        elif not is_array(boxes, exclude_numpy_ndarray=True):
            # boxes does not have a valid type
            raise ValueError("'boxes' should be a Box or list of Boxes")

        # boxes contains only Box items
        for box in boxes:
            if not isinstance(box, Box):
                raise ValueError("'boxes' should not contain non-Box items")

        # boxes all have the same dimensionality
        num_dimensions = boxes[0].num_dimensions
        for box in boxes[1:]:
            if box.num_dimensions != num_dimensions:
                raise ValueError("All Box objects in 'boxes' should have "
                                 "the same 'num_dimensions' value")

        # check factor parameter
        if is_scalar(factor):
            # factor is an integer value
            if factor % 1 != 0:
                raise ValueError("When 'factor' is a scalar, it should be an "
                                 "integer")

        elif is_array(factor):
            # factor is not empty
            if array_is_empty(factor):
                raise ValueError("When 'factor' is an array, it should not "
                                 "be empty")

            # factor contains only integer values
            if not contains_only_integers(factor):
                raise ValueError("When 'factor' is an array, it should "
                                 "contain only integer values")

            # len(factor) == num_dimensions
            if len(factor) != num_dimensions:
                raise ValueError("When 'factor' is an array, its length "
                                 "should be equal to the dimensionality of "
                                 "the Box items in 'boxes'")
        else:
            # factor does not have a valid type
            raise ValueError("'factor' should be an int, list-like, or a "
                             "numpy.ndarray")

        # --- Preparations

        # Convert factor to numpy.ndarray
        factor = factor * numpy.ones(num_dimensions, dtype='int')

        # --- Coarsen boxes

        coarsened_boxes = []
        for box in boxes:
            coarsened_boxes.append(Box(box.lower // factor,
                                       box.upper // factor))

        return coarsened_boxes

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
        >>> lower = (0, 0, 0)
        >>> upper = (10, 10, 10)
        >>> box = Box(lower, upper)
        >>> print(box)
        Box([0, 0, 0], [10, 10, 10])
        """
        return "Box({}, {})".format(list(self.lower), list(self.upper))

    def __eq__(self, other):
        """
        Return whether 'other' is an equivalent object.

        Parameters
        ----------
        other: object
            object to compare with

        Return value
        ------------
        bool: True if 'other' is an equivalent object; False otherwise

        Examples
        --------
        >>> lower = (0, 0, 0)
        >>> upper = (10, 10, 10)
        >>> box = Box(lower, upper)
        >>> equivalent_box = Box(lower, upper)
        >>> box == equivalent_box
        True
        >>> box is equivalent_box
        False
        """
        if isinstance(other, self.__class__):
            return numpy.all(self.lower == other.lower) and \
                   numpy.all(self.upper == other.upper)

        return False
