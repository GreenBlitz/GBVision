from gbvision.utils.shapes.base_ellipse import BaseEllipse
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawEllipses(DrawShapes):
    """
    A pipeline that draws all ellipses according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseEllipse
