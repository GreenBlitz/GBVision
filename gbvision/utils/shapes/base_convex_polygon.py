from .base_polygon import BasePolygon
from gbvision.constants.types import Polygon
from gbvision.models.shapes import convex_shape_collision


class BaseConvexPolygon(BasePolygon):

    @staticmethod
    def shape_collision(shape1: Polygon, shape2: Polygon) -> bool:
        return convex_shape_collision(shape1, shape2)
