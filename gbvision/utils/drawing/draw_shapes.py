import abc
from typing import Callable, List

from gbvision.constants.types import Frame, Shape, Color
from gbvision.utils.pipeline import PipeLine
from gbvision.utils.shapes.base_shape import BaseShapeType


class DrawShapes(PipeLine, abc.ABC):
    """
    An abstract pipeline class that receives a frame, finds all shapes in a frame using the finding func, draws
    all shapes on a copy of the frame and returns the copy

    :param finding_func: A function that receives a frame and returns a list of the shape, used to find the shapes
                         to draw
    :param color: The color to draw with
    :param args: Optional additional args to pass to BaseShape.draw_multiple
    :param kwargs: Optional additional kwargs to pass to BaseShape.draw_multiple
    """

    def __init__(self, finding_func: Callable[[Frame], List[Shape]], color: Color, *args, **kwargs):
        self.finding_func = finding_func
        self.color = color
        self.args = args
        self.kwargs = kwargs
        PipeLine.__init__(self, self.draw)

    def draw(self, frame: Frame) -> Frame:
        """
        Finds the shapes using the finding func and draws them on a copy of the frame

        :param frame: The frame to draw on
        :return: A copy of the frame, with all the shapes drawn on it
        """
        return self._base_shape().draw_multiple(frame, self.finding_func(frame), self.color, *self.args, **self.kwargs)

    @staticmethod
    @abc.abstractmethod
    def _base_shape() -> BaseShapeType:
        """
        :return: A BaseShape of this shape
        """
