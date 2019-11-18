from copy import deepcopy

from gbvision.models.shapes import rect_collision
from gbvision.constants.types import *
from gbvision.continuity.continues_shape import ContinuesShape


# TODO add docs

class ContinuesRect(ContinuesShape):
    def __init__(self, shape: Rect, *args, **kwargs):
        ContinuesShape.__init__(self, shape=shape, *args, **kwargs)

    def _shape_collision(self, shape) -> bool:
        return rect_collision(self._shape, shape)

    @staticmethod
    def _shape_area(rect: Rect) -> Number:
        return rect[2] * rect[3]

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect):
        return deepcopy(bounding_rect)

    @staticmethod
    def _to_bounding_rect(rect: Rect) -> Rect:
        return deepcopy(rect)

    @staticmethod
    def _shape_center(shape: Rect) -> Point:
        center_x = shape[0] + shape[2] / 2
        center_y = shape[1] + shape[3] / 2
        return center_x, center_y
