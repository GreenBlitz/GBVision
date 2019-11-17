import math

from gbvision.models.shapes import rotated_rect_collision
from gbvision.constants.types import Rect, Number, Ellipse
from gbvision.continuity.continues_shape import ContinuesShape


class ContinuesEllipse(ContinuesShape):
    @staticmethod
    def _to_bounding_rect(shape: Ellipse) -> Rect:
        return [shape[0] - shape[2], shape[1] - shape[3], 2 * shape[2], 2 * shape[3]]

    def _shape_collision(self, shape: Ellipse) -> bool:
        return rotated_rect_collision()
    
    @staticmethod
    def _shape_square_distance(self, elp: Ellipse) -> Number:
        return (elp[0] - self._shape[0])**2 + (elp[1] - self._shape[1])**2

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect) -> Ellipse:
        return [bounding_rect[0] + bounding_rect[2]/2, bounding_rect[1] + bounding_rect[3]/2, bounding_rect[2]/2, bounding_rect[3]/2]


def _shape_area(shape: Ellipse) -> Number:
    return math.pi * shape[2] * shape[3]


@staticmethod
def _to_bounding_rect(elp: Ellipse) -> Rect:
    return [elp[0] - elp[2]/2, elp[1] - elp[3]/2, elp[0]*2, elp[1]*2]
