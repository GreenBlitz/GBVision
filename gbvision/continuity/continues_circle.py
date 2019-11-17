import math

from gbvision.models.shapes import circle_collision
from gbvision.constants.types import Rect, Number, Circle
from gbvision.continuity.continues_shape import ContinuesShape
from gbvision.utils.tracker import Tracker


class ContinuesCircle(ContinuesShape):
    def __init__(self, shape: Circle, *args, **kwargs):
        ContinuesShape.__init__(self, shape=shape, *args, **kwargs)

    def _shape_collision(self, shape: Circle) -> bool:
        return circle_collision(self._shape, shape)

    @staticmethod
    def _shape_area(shape: Circle) -> Number:
        return math.pi * shape[1] ** 2

    def _shape_square_distance(self, shape: Circle) -> Number:
        return (self._shape[0][0] - shape[0][0]) ** 2 + (self._shape[0][1] - shape[0][1]) ** 2

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect) -> Circle:
        circle = (
            (bounding_rect[0] + bounding_rect[2] / 2, bounding_rect[1] + bounding_rect[3] / 2),
            (bounding_rect[3] + bounding_rect[2]) / 4)
        return circle

    @staticmethod
    def _to_bounding_rect(shape: Circle) -> Rect:
        rect = (shape[0][0] - shape[1], shape[0][1] - shape[1], 2 * shape[1], 2 * shape[1])
        return rect
