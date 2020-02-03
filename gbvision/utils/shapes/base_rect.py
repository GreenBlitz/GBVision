from .base_shape import BaseShape
from gbvision.constants.types import Rect, Number, Point
from gbvision.models.shapes import rect_collision


class BaseRect(BaseShape):
    @staticmethod
    def shape_center(shape: Rect) -> Point:
        return shape[0] + (shape[2] / 2), shape[1] + (shape[3] / 2)

    @staticmethod
    def shape_collision(shape1: Rect, shape2: Rect) -> bool:
        return rect_collision(shape1, shape2)

    @classmethod
    def shape_area(cls, shape: Rect) -> Number:
        return shape[2] * shape[3]
