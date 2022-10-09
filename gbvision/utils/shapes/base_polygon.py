from typing import List

import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Polygon, Number, Point, Contour, Shape
from gbvision.models.contours import contour_center, contours_to_polygons


class BasePolygon(BaseShape):
    @staticmethod
    def from_contours(contours: List[Contour]) -> List[Shape]:
        return contours_to_polygons(contours)

    @staticmethod
    def area(shape: Polygon) -> Number:
        return cv2.contourArea(shape)

    @staticmethod
    def center(shape: Polygon) -> Point:
        return contour_center(shape)

    @staticmethod
    def shape_collision(shape1: Polygon, shape2: Polygon) -> bool:
        return NotImplemented

