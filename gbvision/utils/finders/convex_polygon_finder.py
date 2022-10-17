from .object_finder import ShapeFinder
from gbvision.utils.shapes.base_convex_polygon import BaseConvexPolygon


class ConvexPolygonFinder(ShapeFinder):
    """
    Finds any generic convex polygon, not recommended when another finder can be used
    """

    @staticmethod
    def _base_shape():
        return BaseConvexPolygon
