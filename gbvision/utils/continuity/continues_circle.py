from .continues_shape import ContinuesShape
from gbvision.utils.shapes.base_circle import BaseCircle


class ContinuesCircle(ContinuesShape):
    """
    An implementation of ContinuesShape to circles.
    used to try and check whether two circles are indeed the same one.
    """

    @staticmethod
    def _base_shape():
        return BaseCircle

