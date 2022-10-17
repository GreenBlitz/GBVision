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
