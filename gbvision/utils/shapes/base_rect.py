from typing import List

from .base_shape import BaseShape
from gbvision.constants.types import Rect, Number, Point
from gbvision.models.shapes import rect_collision
from gbvision.models.contours import contours_to_rects
from gbvision.constants.types import Contour


class BaseRect(BaseShape):
    @staticmethod
    def from_contours(cnts: List[Contour]) -> List[Rect]:
        return contours_to_rects(cnts)

    @staticmethod
    def center(shape: Rect) -> Point:
        return shape[0] + (shape[2] / 2), shape[1] + (shape[3] / 2)

    @staticmethod
    def collision(shape1: Rect, shape2: Rect) -> bool:
        return rect_collision(shape1, shape2)

    @classmethod
    def area(cls, shape: Rect) -> Number:
        return shape[2] * shape[3]
