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

