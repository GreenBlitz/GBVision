import cv2

from .base_contour import BaseContour
from gbvision.constants.types import Polygon, Contour


class BasePolygon(BaseContour):
    @staticmethod
    def from_contour(cnt: Contour, arc_length_multiplier=0.05) -> Polygon:
        arc_length = arc_length_multiplier * cv2.arcLength(cnt, True)
        return cv2.approxPolyDP(cnt, arc_length, True)
