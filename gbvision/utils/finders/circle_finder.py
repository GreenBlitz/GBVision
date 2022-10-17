from .object_finder import ShapeFinder
from gbvision.utils.shapes.base_circle import BaseCircle
from ..shapes.base_shape import BaseShapeType


class CircleFinder(ShapeFinder):
    """
    Finds specific circular shaped object, and performs distance transformation
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseCircle
