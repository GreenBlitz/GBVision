import abc
from typing import Type, List, Union

import numpy as np

from gbvision.constants.types import Shape, Number, Rect, Point, Contour, Frame, Color


class BaseShape(abc.ABC):
    def __init__(self):
        raise Exception("Can't create an instance of a base shape class")

    @staticmethod
    @abc.abstractmethod
    def to_bounding_rect(shape: Shape) -> Rect:
        """
        Finds the bounding rect of this shape

        :param shape: The shape
        :return: The bounding rect of this shape, as a gbvision.Rect
        """

    @staticmethod
    @abc.abstractmethod
    def from_bounding_rect(bounding_rect: Rect) -> Shape:
        """
        Converts a rect to the closest possible object of this shape that is contained in it

        :param bounding_rect: The rect to convert
        :return: A shape of this type that is as close as possible to this rect
        """

    @staticmethod
    @abc.abstractmethod
    def from_contour(cnt: Contour) -> Shape:
        """
        Converts a single contour to this shape

        :param cnt: The contour
        :return: A shape representing this contour
        """

    @classmethod
    def from_contours(cls, cnts: List[Contour]) -> List[Shape]:
        """
        Converts the given list of contours to a list of this shape

        :param cnts: The contours to convert
        :return: A list of this shape, the same length as the contours list
        """
        return list(map(cls.from_contour, cnts))

    @staticmethod
    @abc.abstractmethod
    def collision(shape1: Shape, shape2: Shape) -> bool:
        """
        checks if the two shapes are colliding

        :param shape1: the first shape
        :param shape2: the second shape
        :return: True if the shapes are colliding, False otherwise
        """

    @staticmethod
    @abc.abstractmethod
    def area(shape: Shape) -> Number:
        """
        calculates the area of the shape

        :param shape: the shape
        :return: the area of the shape
        """

    @staticmethod
    @abc.abstractmethod
    def center(shape: Shape) -> Point:
        """
        calculates the center-of-mass of the shape

        :param shape: the shape
        :return: the center of the shape
        """

    @classmethod
    def root_area(cls, shape: Shape) -> Number:
        """
        calculates the square root of the area of the shape
        default is the square root of cls.shape_area, but it can be overridden in case there is a simpler way\
         (for example for circles)

        :param shape: the shape
        :return: the square root of the area of the shape
        """
        return np.sqrt(cls.area(shape))

    @classmethod
    def sort(cls, shapes: List[Shape]) -> List[Shape]:
        """
        sorts the list of shapes by area, should be overridden to use area root in case it's better
        doesn't modify the given list, returns a new list

        :param shapes: the list of shapes to sort
        :return: a sorted copy of the list of shapes
        """
        return sorted(shapes, key=cls.area, reverse=True)

    @classmethod
    def filter_inners(cls, shapes: List[Shape]) -> List[Shape]:
        """
        filters out all shapes that are colliding with a shape with a smaller index in the given list
        returns a list of all shapes that aren't colliding

        :param shapes: the list of shapes
        :return: the filtered list of shapes
        """
        filtered_shapes = []
        for i, shape in enumerate(shapes):
            shape_invalid = False
            for j in range(i):
                shape_invalid = cls.collision(shape, shapes[j])
                if shape_invalid:
                    break
            if not shape_invalid:
                filtered_shapes.append(shape)
        return filtered_shapes

    @classmethod
    def from_contours_sorted(cls, cnts: List[Contour]) -> List[Shape]:
        """
        Converts the given list of contours to a list of this shape, and sorts them by size

        :param cnts: The contours to convert
        :return: A list of this shape, the same length as the contours list
        """
        return cls.sort(cls.from_contours(cnts))

    @classmethod
    def distance_squared(cls, shape1: Shape, shape2: Shape) -> Number:
        """
        Finds the square of the distance between the centers of the shapes

        :param shape1: The first shape
        :param shape2: The second shape
        :return: The square of distance between the two centers
        """
        center1 = cls.center(shape1)
        center2 = cls.center(shape2)
        return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2

    @classmethod
    def distance(cls, shape1: Shape, shape2: Shape) -> Number:
        """
        Finds the square of the distance between the centers of the shapes

        :param shape1: The first shape
        :param shape2: The second shape
        :return: The square of distance between the two centers
        """
        return np.sqrt(cls.distance_squared(shape1, shape2))

    @staticmethod
    @abc.abstractmethod
    def _unsafe_draw(frame: Frame, shape: Shape, color: Color, *args, **kwargs) -> None:
        """
        Unsafely draws this shape on the frame
        This method should modify the given frame and not return anything

        :param frame: The frame to draw on
        :param shape: The shape to draw
        :param color: The color to draw with
        :param args: Optional arguments to pass to the drawing function
        :param kwargs: Optional keyword arguments to pass to the drawing function
        """

    @classmethod
    def _unsafe_draw_multiple(cls, frame: Frame, shapes: List[Shape], color: Color, *args, **kwargs) -> None:
        """
        Unsafely draws this object on the frame
        This method should modify the given frame and not return anything

        :param frame: The frame to draw on
        :param shapes: The list of shapes to draw
        :param color: The color to draw with
        :param args: Optional arguments to pass to the drawing function
        :param kwargs: Optional keyword arguments to pass to the drawing function
        """
        for shape in shapes:
            cls._unsafe_draw(frame, shape, color, *args, **kwargs)

    @classmethod
    def draw(cls, frame: Frame, shape: Shape, color: Color, *args, **kwargs) -> Frame:
        """
        Draws the given shape on the frame
        This method does not change to original frame, and instead creates a copy of it and returns the copy

        :param frame: The frame to draw on
        :param shape: The shape to draw
        :param color: The color to use
        :param args: Optional arguments to pass to the drawing function
        :param kwargs: Optional keyword arguments to pass to the drawing function
        :return: A copy of the frame with the shape drawn on it
        """
        frame = frame.copy()
        cls._unsafe_draw(frame, shape, color, *args, **kwargs)
        return frame

    @staticmethod
    @abc.abstractmethod
    def set_center(shape: Shape, new_center: Point) -> Shape:
        """
        Returns an identical copy that has been moved to a new location
        Only the center should be different

        :param shape: The shape
        :param new_center: The new center, calling BaseShape.center on the return value should result in this
        :return: A copy of this shape, with the new center
        """

    @classmethod
    def draw_multiple(cls, frame: Frame, shapes: List[Shape], color: Color, *args, **kwargs) -> Frame:
        """
        Draws the given shapes on the frame
        This method does not change to original frame, and instead creates a copy of it and returns the copy

        :param frame: The frame to draw on
        :param shapes: The list of shapes to draw
        :param color: The color to use
        :param args: Optional arguments to pass to the drawing function
        :param kwargs: Optional keyword arguments to pass to the drawing function
        :return: A copy of the frame with the shape drawn on it
        """
        frame = frame.copy()
        cls._unsafe_draw_multiple(frame, shapes, color, *args, **kwargs)
        return frame


BaseShapeType = Type[BaseShape]
