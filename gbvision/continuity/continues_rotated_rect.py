from copy import deepcopy

import numpy

from gbvision.models.shapes import rotated_rect_collision
from gbvision.constants.types import *
from gbvision.continuity.continues_shape import ContinuesShape


# TODO add docs

class ContinuesRotatedRect(ContinuesShape):
    def __init__(self, shape: RotatedRect, *args, **kwargs):
        ContinuesShape.__init__(self, shape=shape, *args, **kwargs)

    def _shape_collision(self, shape) -> bool:
        return rotated_rect_collision(self._shape, shape)

    @staticmethod
    def _shape_area(rect: Rect) -> Number:
        return rect[1][0] * rect[1][1]

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect):

    # needs angle

    @staticmethod
    def _to_bounding_rect(rotated_rect: Rect) -> Rect:
        x = rotated_rect[0][0]
        y = rotated_rect[0][1]
        w = rotated_rect[1][0]
        h = rotated_rect[1][1]
        a = rotated_rect[2]

        bound_w = w * numpy.cos(a) + h * numpy.sin(a)
        bound_h = h * numpy.cos(a) + w * numpy.sin(a)
        bound_x = x - bound_w / 2
        bound_y = y - bound_h / 2
        return Rect(bound_x, bound_y, bound_w, bound_h)

    def _shape_square_distance(self, rect: Rect) -> Number:
        return (self._get_center(rect)[0] - self._get_center(self._shape)[0]) ** 2 + \
               (self._get_center(rect)[1] - self._get_center(self._shape)[1]) ** 2

    @staticmethod
    def _get_center(rotated_rect: RotatedRect) -> Point:
        return rotated_rect[0][0], rotated_rect[0][1]
