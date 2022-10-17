from gbvision.utils.shapes.base_line import BaseLine
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawLines(DrawShapes):
    """
    A pipeline that draws all lines according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseLine
