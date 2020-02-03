import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Polygon, Number, Point
from gbvision.models.contours import contour_center


class BasePolygon(BaseShape):
    @staticmethod
    def shape_area(shape: Polygon) -> Number:
        return cv2.contourArea(shape)

    @staticmethod
    def shape_center(shape: Polygon) -> Point:
        return contour_center(shape)

    @staticmethod
    def shape_collision(shape1: Polygon, shape2: Polygon) -> bool:
        return NotImplemented

