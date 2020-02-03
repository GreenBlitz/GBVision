from copy import deepcopy

from gbvision.models.shapes import rect_collision
from gbvision.constants.types import Rect
from .continues_shape import ContinuesShape
from gbvision.utils.shapes.base_rect import BaseRect


class ContinuesRect(ContinuesShape):
    """
    An implementation of ContinuesShape to rectangles.
    used to try and check whether two rectangles are indeed the same one.
    """

    @staticmethod
    def _base_shape():
        return BaseRect

    def __init__(self, shape: Rect, *args, **kwargs):
        ContinuesShape.__init__(self, shape=shape, *args, **kwargs)

    def _shape_collision(self, shape) -> bool:
        return rect_collision(self._shape, shape)

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect):
        return deepcopy(bounding_rect)

    @staticmethod
    def _to_bounding_rect(rect: Rect) -> Rect:
        return deepcopy(rect)
