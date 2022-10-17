from gbvision.utils.shapes.base_point import BasePoint
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawPoints(DrawShapes):
    """
    A pipeline that draws all points according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BasePoint
