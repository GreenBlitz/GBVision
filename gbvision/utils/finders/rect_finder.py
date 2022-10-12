from .object_finder import ObjectFinder
from gbvision.utils.shapes.base_rect import BaseRect
from ..shapes.base_shape import BaseShapeType


class RectFinder(ObjectFinder):
    """
    Finds a rectangular shaped object
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRect
