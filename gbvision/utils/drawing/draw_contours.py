from gbvision.utils.shapes.base_contour import BaseContour
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawContours(DrawShapes):
    """
    A pipeline that draws all contours according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseContour
