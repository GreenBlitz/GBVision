from copy import deepcopy

from gbvision.models.shapes import rect_collision
from gbvision.constants.types import *
from gbvision.continuity.continues_shape import ContinuesShape
from gbvision.utils.tracker import Tracker


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

    def _shape_square_distance(self, rect: Rect) -> Number:
        return (self._get_center(rect)[0] - self._get_center(self._shape)[0]) ** 2 + (
                    self._get_center(rect)[1] - self._get_center(self._shape)[1]) ** 2

    @staticmethod
    def _get_center(rect: Rect) -> Point:
        center_x = (rect[0] + rect[3]) / 2
        center_y = (rect[1] + rect[4]) / 2
        return center_x, center_y
