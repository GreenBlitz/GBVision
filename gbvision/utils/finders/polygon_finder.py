from .object_finder import ShapeFinder
from gbvision.utils.shapes.base_polygon import BasePolygon
from ..shapes.base_shape import BaseShapeType


class PolygonFinder(ShapeFinder):
    """
    Finds any generic polygon, not recommended when another finder can be used
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BasePolygon
