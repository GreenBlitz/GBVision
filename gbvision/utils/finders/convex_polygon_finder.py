from .object_finder import ObjectFinder
from gbvision.utils.shapes.base_convex_polygon import BaseConvexPolygon


class ConvexPolygonFinder(ObjectFinder):
    """
    Finds any generic convex polygon, not recommended when another finder can be used
    """

    @staticmethod
    def _base_shape():
        return BaseConvexPolygon
