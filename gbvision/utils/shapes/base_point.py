from copy import deepcopy

from .base_shape import BaseShape
from .base_circle import BaseCircle
from .base_rect import BaseRect
from gbvision.constants.types import Number, Point, Frame, Color, Rect, Contour


class BasePoint(BaseShape):
    @staticmethod
    def set_center(shape: Point, new_center: Point) -> Point:
        return deepcopy(new_center)

    @staticmethod
    def _unsafe_draw(frame: Frame, shape: Point, color: Color, *args, **kwargs) -> None:
        BaseCircle.draw(frame, (shape, 1), color, *args, **kwargs)

    @staticmethod
    def to_bounding_rect(shape: Point) -> Rect:
        return shape[0] - 1, shape[1] - 1, 2, 2

    @staticmethod
    def from_bounding_rect(bounding_rect: Rect) -> Point:
        return BaseRect.center(bounding_rect)

    @staticmethod
    def from_contour(cnt: Contour) -> Point:
        # Cannot convert a contour to a point
        return NotImplemented

    @staticmethod
    def center(shape: Point) -> Point:
        return deepcopy(shape)

    @staticmethod
    def collision(shape1: Point, shape2: Point) -> bool:
        return shape1[0] == shape2[0] and shape1[1] == shape2[1]

    @classmethod
    def area(cls, shape: Point) -> Number:
        # A point has no area
        return 0

    @staticmethod
    def rotate(shape: Point, angle: Number) -> Point:
        """
        Rotates the point around the (0, 0) point by the given angle

        :param shape: The point to rotate
        :param angle: The angle by which to rotate
        :return: The point after rotation
        """
        return 0, 0