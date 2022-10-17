from copy import deepcopy

import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Rect, Number, Point, Frame, Color


class BaseRect(BaseShape):
    @classmethod
    def set_center(cls, shape: Rect, new_center: Point) -> Rect:
        current_center = cls.center(shape)
        center_diff = new_center[0] - current_center[0], new_center[1] - current_center[1]
        return shape[0] + center_diff[0], shape[1] + center_diff[1], shape[2], shape[3]

    @staticmethod
    def _unsafe_draw(frame: Frame, shape: Rect, color: Color, *args, **kwargs) -> None:
        cv2.rectangle(frame, (int(shape[0]), int(shape[1])), (int(shape[0] + shape[2]), int(shape[1] + shape[3])),
                      color, *args, **kwargs)

    @staticmethod
    def to_bounding_rect(shape: Rect) -> Rect:
        return deepcopy(shape)

    @staticmethod
    def from_bounding_rect(bounding_rect: Rect) -> Rect:
        return deepcopy(bounding_rect)

    from_contour = cv2.boundingRect

    @staticmethod
    def center(shape: Rect) -> Point:
        return shape[0] + (shape[2] / 2), shape[1] + (shape[3] / 2)

    @staticmethod
    def collision(shape1: Rect, shape2: Rect) -> bool:
        return not (shape1[0] > shape2[0] + shape2[2] or
                    shape1[0] + shape1[2] < shape1[0] or
                    shape1[1] > shape2[1] + shape2[3] or
                    shape1[1] + shape1[3] < shape2[1])

    @classmethod
    def area(cls, shape: Rect) -> Number:
        return shape[2] * shape[3]
