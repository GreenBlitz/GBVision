from gbvision.constants.types import Circle
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

    def __init__(self, shape: Circle, *args, **kwargs):
        ContinuesShape.__init__(self, shape, *args, **kwargs)
