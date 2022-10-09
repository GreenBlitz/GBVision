from typing import List

from gbvision.constants.math import SQRT_PI

from .base_shape import BaseShape
from gbvision.constants.types import Circle, Number, Point
from gbvision.models.shapes import circle_collision
from ... import Contour, Shape, contours_to_circles


class BaseCircle(BaseShape):
    @staticmethod
    def from_contours(contours: List[Contour]) -> List[Shape]:
        return contours_to_circles(contours)

    @staticmethod
    def center(shape: Circle) -> Point:
        return shape[0]

    @staticmethod
    def shape_collision(shape1: Circle, shape2: Circle) -> bool:
        return circle_collision(shape1, shape2)

    @classmethod
    def area(cls, shape: Circle) -> Number:
        return cls.root_area(shape) ** 2

    @classmethod
    def root_area(cls, shape: Circle) -> Number:
        return shape[1] * SQRT_PI

    @classmethod
    def sort(cls, shapes: List[Circle]):
        return sorted(shapes, key=cls.root_area)
