import abc
from typing import Type, List

import numpy as np

from gbvision.constants.types import Shape, Number, Rect, Point


class BaseShape(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def shape_collision(shape1: Shape, shape2: Shape) -> bool:
        """
        checks if the two shapes are colliding

        :param shape1: the first shape
        :param shape2: the second shape
        :return: True if the shapes are colliding, False otherwise
        """

    @staticmethod
    @abc.abstractmethod
    def shape_area(shape: Shape) -> Number:
        """
        calculates the area of the shape

        :param shape: the shape
        :return: the area of the shape
        """

    @staticmethod
    @abc.abstractmethod
    def shape_center(shape: Shape) -> Point:
        """
        calculates the center-of-mass of the shape

        :param shape: the shape
        :return: the center of the shape
        """

    @classmethod
    def shape_root_area(cls, shape: Shape) -> Number:
        """
        calculates the square root of the area of the shape
        default is the square root of cls.shape_area, but it can be overridden in case there is a simpler way\
         (for example for circles)

        :param shape: the shape
        :return: the square root of the area of the shape
        """
        return np.sqrt(cls.shape_area(shape))

    @classmethod
    def sort_shapes(cls, shapes: List[Shape]) -> List[Shape]:
        """
        sorts the list of shapes by area, should be overridden to use area root in case it's better
        doesn't modify the given list, returns a new list

        :param shapes: the list of shapes to sort
        :return: a sorted copy of the list of shapes
        """
        return sorted(shapes, key=cls.shape_area, reverse=True)

    @classmethod
    def filter_inner_shapes(cls, shapes: List[Shape]) -> List[Shape]:
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
                shape_invalid = cls.shape_collision(shape, shapes[j])
                if shape_invalid:
                    break
            if not shape_invalid:
                filtered_shapes.append(shape)
        return filtered_shapes


BaseShapeType = Type[BaseShape]
