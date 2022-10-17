from gbvision.utils.shapes.base_rect import BaseRect
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawRects(DrawShapes):
    """
    A pipeline that draws all rects according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRect
