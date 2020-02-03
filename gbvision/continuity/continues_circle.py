import numpy as np

from gbvision.models.shapes import circle_collision
from gbvision.constants.types import Rect, Number, Circle, Point
from gbvision.continuity.continues_shape import ContinuesShape


class ContinuesCircle(ContinuesShape):
    """
    An implementation of ContinuesShape to circles.
    used to try and check whether two circles are indeed the same one.
    """

    @staticmethod
    def _shape_center(shape) -> Point:
        return shape[0]

    def __init__(self, shape: Circle, *args, **kwargs):
        ContinuesShape.__init__(self, shape, *args, **kwargs)

    def _shape_collision(self, shape) -> bool:
        return circle_collision(self._shape, shape)

    @staticmethod
    def _shape_area(shape: Circle) -> Number:
        return np.pi * shape[1] * shape[1]

    @staticmethod
    def _from_bounding_rect(bounding_rect) -> Circle:
        circle = (
            (bounding_rect[0] + bounding_rect[2] / 2, bounding_rect[1] + bounding_rect[3] / 2),
            (bounding_rect[3] + bounding_rect[2]) / 4)
        return circle

    @staticmethod
    def _to_bounding_rect(shape) -> Rect:
        rect = (shape[0][0] - shape[1], shape[0][1] - shape[1], 2 * shape[1], 2 * shape[1])
        return rect
