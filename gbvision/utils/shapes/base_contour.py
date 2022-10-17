from copy import deepcopy
from typing import List

import numpy as np
import cv2

from .base_shape import BaseShape
from .base_rect import BaseRect
from gbvision.constants.types import Contour, Number, Point, Rect, Frame, Color
from gbvision.constants.math import EPSILON


class BaseContour(BaseShape):
    @classmethod
    def set_center(cls, shape: Contour, new_center: Point) -> Contour:
        current_center = cls.center(shape)
        return np.array(shape) + [new_center[0] - current_center[0], new_center[1] - current_center[1]]

    @classmethod
    def _unsafe_draw(cls, frame: Frame, shape: Contour, color: Color, *args, **kwargs) -> None:
        return cls._unsafe_draw_multiple(frame, [shape], color, *args, **kwargs)

    @classmethod
    def _unsafe_draw_multiple(cls, frame: Frame, shapes: List[Contour], color: Color, *args, **kwargs) -> None:
        return cv2.drawContours(frame, shapes, -1, color, *args, **kwargs)

    @staticmethod
    def to_bounding_rect(shape: Contour) -> Rect:
        return BaseRect.from_contour(shape)

    @staticmethod
    def from_bounding_rect(bounding_rect: Rect) -> Contour:
        return np.array([[bounding_rect[0], bounding_rect[1]],
                         [bounding_rect[0] + bounding_rect[2], bounding_rect[1]],
                         [bounding_rect[0] + bounding_rect[2], bounding_rect[1] + bounding_rect[3]],
                         [bounding_rect[0], bounding_rect[1] + bounding_rect[3]]])

    @staticmethod
    def from_contour(cnt: Contour) -> Contour:
        return deepcopy(cnt)

    @staticmethod
    def area(shape: Contour) -> Number:
        return cv2.contourArea(shape)

    @staticmethod
    def center(shape: Contour) -> Point:
        m = cv2.moments(shape)
        return int(m['m10'] / (m['m00'] + EPSILON)), int(m['m01'] / (m['m00'] + EPSILON))

    @staticmethod
    def collision(shape1: Contour, shape2: Contour) -> bool:
        return NotImplemented

