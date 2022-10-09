from typing import List

import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Contour, Number, Point
from gbvision.models.contours import contour_center
from ... import Shape


class BaseContour(BaseShape):
    @staticmethod
    def from_contours(contours: List[Contour]) -> List[Shape]:
        return contours

    @staticmethod
    def area(shape: Contour) -> Number:
        return cv2.contourArea(shape)

    @staticmethod
    def center(shape: Contour) -> Point:
        return contour_center(shape)

    @staticmethod
    def shape_collision(shape1: Contour, shape2: Contour) -> bool:
        return NotImplemented

