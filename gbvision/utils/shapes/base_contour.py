from typing import List

import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Contour, Number, Point
from gbvision.models.contours import contour_center


class BaseContour(BaseShape):
    @staticmethod
    def from_contours(cnts: List[Contour]) -> List[Contour]:
        return cnts

    @staticmethod
    def area(shape: Contour) -> Number:
        return cv2.contourArea(shape)

    @staticmethod
    def center(shape: Contour) -> Point:
        return contour_center(shape)

    @staticmethod
    def collision(shape1: Contour, shape2: Contour) -> bool:
        return NotImplemented

