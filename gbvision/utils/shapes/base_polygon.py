from typing import List

import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Polygon, Number, Point
from gbvision.models.contours import contour_center
from gbvision.models.contours import contours_to_polygons
from gbvision.constants.types import Contour


class BasePolygon(BaseShape):
    @staticmethod
    def from_contours(cnts: List[Contour]) -> List[Polygon]:
        return contours_to_polygons(cnts)

    @staticmethod
    def area(shape: Polygon) -> Number:
        return cv2.contourArea(shape)

    @staticmethod
    def center(shape: Polygon) -> Point:
        return contour_center(shape)

    @staticmethod
    def collision(shape1: Polygon, shape2: Polygon) -> bool:
        return NotImplemented

