from copy import deepcopy

import numpy

from gbvision.models.shapes import rotated_rect_collision
from gbvision.constants.types import RotatedRect, Number, Rect, Point
from gbvision.continuity.continues_shape import ContinuesShape


# TODO add docs

class ContinuesRotatedRect(ContinuesShape):
    def __init__(self, shape: RotatedRect, *args, **kwargs):
        ContinuesShape.__init__(self, shape=shape, *args, **kwargs)

    def _shape_collision(self, shape) -> bool:
        return rotated_rect_collision(self._shape, shape)

    @staticmethod
    def _shape_area(rect: RotatedRect) -> Number:
        return rect[1][0] * rect[1][1]

    @staticmethod
    def _from_bounding_rect(bounding_rect: RotatedRect):
        pass
    # needs angle

    @staticmethod
    def _to_bounding_rect(rotated_rect: RotatedRect) -> Rect:
        x = rotated_rect[0][0]
        y = rotated_rect[0][1]
        w = rotated_rect[1][0]
        h = rotated_rect[1][1]
        a = rotated_rect[2]

        bound_w = w * numpy.cos(a) + h * numpy.sin(a)
        bound_h = h * numpy.cos(a) + w * numpy.sin(a)
        bound_x = x - bound_w / 2
        bound_y = y - bound_h / 2
        return bound_x, bound_y, bound_w, bound_h

    @staticmethod
    def _shape_center(shape: RotatedRect) -> Point:
        return shape[0]
