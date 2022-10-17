from gbvision.utils.shapes.base_rotated_rect import BaseRotatedRect
from gbvision.utils.drawing.draw_shapes import DrawShapes
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawRotatedRects(DrawShapes):
    """
    A pipeline that draws all rotated rects according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRotatedRect
