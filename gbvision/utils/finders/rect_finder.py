from .object_finder import ShapeFinder
from gbvision.utils.shapes.base_rect import BaseRect
from ..shapes.base_shape import BaseShapeType


class RectFinder(ShapeFinder):
    """
    Finds a rectangular shaped object
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRect
