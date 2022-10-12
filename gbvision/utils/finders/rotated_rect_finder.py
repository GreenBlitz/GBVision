from .object_finder import ObjectFinder
from gbvision.utils.shapes.base_rotated_rect import BaseRotatedRect
from ..shapes.base_shape import BaseShapeType


class RotatedRectFinder(ObjectFinder):
    """
    Finds a rectangular object, but rotated.
    Recommended to use when you know the shape isn't parallel to the camera
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRotatedRect
