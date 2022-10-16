import abc
from typing import Callable

from gbvision.constants.types import Frame, Shape, Color
from gbvision.utils.pipeline import PipeLine
from gbvision.utils.shapes.base_shape import BaseShapeType
from gbvision.utils.shapes.base_contour import BaseContour
from gbvision.utils.shapes.base_circle import BaseCircle
from gbvision.utils.shapes.base_rect import BaseRect
from gbvision.utils.shapes.base_rotated_rect import BaseRotatedRect
from gbvision.utils.shapes.base_ellipse import BaseEllipse


class _DrawObject(PipeLine, abc.ABC):
    def __init__(self, finding_func: Callable[[Frame], Shape], color: Color, *args, **kwargs):
        def _draw(frame):
            return self._base_shape().draw_multiple(frame, finding_func(frame), color, *args, **kwargs)

        PipeLine.__init__(self, _draw)

    @staticmethod
    @abc.abstractmethod
    def _base_shape() -> BaseShapeType:
        """
        :return: A BaseShape of this shape
        """


class DrawContours(_DrawObject):
    """
    A pipeline that draws all contours according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseContour


class DrawCircles(_DrawObject):
    """
    A pipeline that draws all circles according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseCircle


class DrawRects(_DrawObject):
    """
    A pipeline that draws all rects according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRect


class DrawRotatedRects(_DrawObject):
    """
    A pipeline that draws all rotated rects according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseRotatedRect


class DrawEllipses(_DrawObject):
    """
    A pipeline that draws all ellipses according to the given parameters, and returns a copy of the frame after drawing
    """

    @staticmethod
    def _base_shape() -> BaseShapeType:
        return BaseEllipse
