from .object_finder import ObjectFinder
from ..shapes.base_contour import BaseContour
from ..shapes.base_shape import BaseShapeType


class ContourFinder(ObjectFinder):
    """
    Finds any generic shape, not recommended when another finder can be used
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseContour
