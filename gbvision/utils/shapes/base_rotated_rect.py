from .base_shape import BaseShape
from gbvision.constants.types import RotatedRect, Number, Point
from gbvision.models.shapes import rotated_rect_collision


class BaseRotatedRect(BaseShape):
    @staticmethod
    def shape_center(shape: RotatedRect) -> Point:
        return shape[0]

    @staticmethod
    def shape_collision(shape1: RotatedRect, shape2: RotatedRect) -> bool:
        return rotated_rect_collision(shape1, shape2)

    @classmethod
    def shape_area(cls, shape: RotatedRect) -> Number:
        return shape[1][0] * shape[1][1]
