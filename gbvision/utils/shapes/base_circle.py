from typing import List

import cv2

from gbvision.constants.math import SQRT_PI

from .base_shape import BaseShape
from gbvision.constants.types import Circle, Number, Point, Rect, Frame, Color


class BaseCircle(BaseShape):
    @staticmethod
    def set_center(shape: Circle, new_center: Point) -> Circle:
        return new_center, shape[1]

    @staticmethod
    def _unsafe_draw(frame: Frame, shape: Circle, color: Color, *args, **kwargs) -> None:
        cv2.circle(frame, (int(shape[0][0]), int(shape[0][1])), int(shape[1]), color, *args, **kwargs)

    @staticmethod
    def to_bounding_rect(shape: Circle) -> Rect:
        rect = (shape[0][0] - shape[1], shape[0][1] - shape[1], 2 * shape[1], 2 * shape[1])
        return rect

    @staticmethod
    def from_bounding_rect(bounding_rect: Rect) -> Circle:
        circle = (
            (bounding_rect[0] + bounding_rect[2] / 2, bounding_rect[1] + bounding_rect[3] / 2),
            (bounding_rect[3] + bounding_rect[2]) / 4)
        return circle

    from_contour = cv2.minEnclosingCircle

    @staticmethod
    def center(shape: Circle) -> Point:
        return shape[0]

    @staticmethod
    def collision(shape1: Circle, shape2: Circle) -> bool:
        center1, r1 = shape1
        center2, r2 = shape2
        return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2 < (r1 + r2) ** 2

    @classmethod
    def area(cls, shape: Circle) -> Number:
        return cls.root_area(shape) ** 2

    @classmethod
    def root_area(cls, shape: Circle) -> Number:
        return shape[1] * SQRT_PI

    @classmethod
    def sort(cls, shapes: List[Circle]):
        return sorted(shapes, key=cls.root_area)
