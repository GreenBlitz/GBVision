import numpy as np
import cv2

from .base_shape import BaseShape
from .base_convex_polygon import BaseConvexPolygon
from gbvision.constants.types import RotatedRect, Number, Point, Rect, Frame, Color


class BaseRotatedRect(BaseShape):
    @staticmethod
    def set_center(shape: RotatedRect, new_center: Point) -> RotatedRect:
        return new_center, shape[1], shape[2]

    @staticmethod
    def _unsafe_draw(frame: Frame, shape: Rect, color: Color, *args, **kwargs) -> None:
        box = cv2.boxPoints(shape)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, color, *args, **kwargs)

    @staticmethod
    def to_bounding_rect(shape: RotatedRect) -> Rect:
        rotated_rect = shape
        x = rotated_rect[0][0]
        y = rotated_rect[0][1]
        w = rotated_rect[1][0]
        h = rotated_rect[1][1]
        a = np.deg2rad(rotated_rect[2])

        bound_w = w * np.cos(a) + h * np.sin(a)
        bound_h = h * np.cos(a) + w * np.sin(a)
        bound_x = x - bound_w / 2
        bound_y = y - bound_h / 2
        return bound_x, bound_y, bound_w, bound_h

    @staticmethod
    def from_bounding_rect(bounding_rect: Rect) -> RotatedRect:
        return ((bounding_rect[0] - bounding_rect[2]) / 2, (bounding_rect[1] + bounding_rect[3] / 2)), \
               bounding_rect[2:4], 0

    from_contour = cv2.minAreaRect

    @staticmethod
    def center(shape: RotatedRect) -> Point:
        return shape[0]

    @staticmethod
    def collision(shape1: RotatedRect, shape2: RotatedRect) -> bool:
        return BaseConvexPolygon.collision(cv2.boxPoints(shape1), cv2.boxPoints(shape2))

    @classmethod
    def area(cls, shape: RotatedRect) -> Number:
        return shape[1][0] * shape[1][1]
