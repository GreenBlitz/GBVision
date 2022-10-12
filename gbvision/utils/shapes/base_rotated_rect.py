from typing import List

from .base_shape import BaseShape
from gbvision.constants.types import RotatedRect, Number, Point
from gbvision.models.shapes import rotated_rect_collision
from gbvision.models.contours import contours_to_rotated_rects
from gbvision.constants.types import Contour


class BaseRotatedRect(BaseShape):
    @staticmethod
    def from_contours(cnts: List[Contour]) -> List[RotatedRect]:
        return contours_to_rotated_rects(cnts)

    @staticmethod
    def center(shape: RotatedRect) -> Point:
        return shape[0]

    @staticmethod
    def collision(shape1: RotatedRect, shape2: RotatedRect) -> bool:
        return rotated_rect_collision(shape1, shape2)

    @classmethod
    def area(cls, shape: RotatedRect) -> Number:
        return shape[1][0] * shape[1][1]
