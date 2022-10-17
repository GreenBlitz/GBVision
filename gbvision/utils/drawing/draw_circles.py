from gbvision.utils.shapes.base_circle import BaseCircle
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawCircles(DrawShapes):
    """
    A pipeline that draws all circles according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseCircle

