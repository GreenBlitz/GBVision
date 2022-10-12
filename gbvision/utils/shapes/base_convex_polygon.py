from .base_polygon import BasePolygon
from gbvision.constants.types import Polygon
from gbvision.models.shapes import convex_shape_collision
from gbvision.models.contours import convex_hull_multiple
from gbvision.utils import PipeLine


class BaseConvexPolygon(BasePolygon):
    @staticmethod
    def collision(shape1: Polygon, shape2: Polygon) -> bool:
        return convex_shape_collision(shape1, shape2)

    from_contours = PipeLine(BasePolygon.from_contours, convex_hull_multiple)
