import numpy as np

from gbvision.models.shapes import rotated_rect_collision
from gbvision.constants.types import RotatedRect, Rect
from .continues_shape import ContinuesShape
from gbvision.utils.shapes.base_rotated_rect import BaseRotatedRect


class ContinuesRotatedRect(ContinuesShape):
    """
    An implementation of ContinuesShape to rotated rectangles.
    used to try and check whether two rotated rectangles are indeed the same one.
    """

    @staticmethod
    def _base_shape():
        return BaseRotatedRect

    def __init__(self, shape: RotatedRect, *args, **kwargs):
        ContinuesShape.__init__(self, shape=shape, *args, **kwargs)

    def _shape_collision(self, shape) -> bool:
        return rotated_rect_collision(self._shape, shape)

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect) -> RotatedRect:
        # assuming the tilting angle is 0
        return ((bounding_rect[0] - bounding_rect[2]) / 2, (bounding_rect[1] + bounding_rect[3] / 2)), \
               bounding_rect[2:4], 0

    @staticmethod
    def _to_bounding_rect(rotated_rect: RotatedRect) -> Rect:
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
