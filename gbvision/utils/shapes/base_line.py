import numpy as np
import cv2

from .base_shape import BaseShape
from gbvision.constants.types import Line, Number, Point, Frame, Color, Rect, Contour
from gbvision.tools.math_tools import almost_equal


class BaseLine(BaseShape):
    @classmethod
    def set_center(cls, shape: Line, new_center: Point) -> Line:
        current_center = cls.center(shape)
        center_diff = new_center[0] - current_center[0], new_center[1] - current_center[1]
        return (shape[0][0] + center_diff[0], shape[0][1] + center_diff[1]), (
            shape[1][0] + center_diff[0], shape[1][1] + center_diff[1])

    @staticmethod
    def _unsafe_draw(frame: Frame, shape: Line, color: Color, *args, **kwargs) -> None:
        cv2.line(frame, shape[0], shape[1], color, *args, **kwargs)

    @staticmethod
    def to_bounding_rect(shape: Line) -> Rect:
        return min(shape[0][0], shape[1][0]), min(shape[0][1], shape[1][1]), abs(shape[0][0] - shape[1][0]), abs(
            shape[0][1] - shape[1][1])

    @staticmethod
    def from_bounding_rect(bounding_rect: Rect) -> Line:
        # There is no way of knowing if the line was top-left to bottom-right or top-right to bottom-left
        return NotImplemented

    @staticmethod
    def from_contour(cnt: Contour) -> Line:
        # Cant convert a contour to a line
        return NotImplemented

    @staticmethod
    def center(shape: Line) -> Point:
        return (shape[0][0] + shape[1][0]) / 2, (shape[0][1] + shape[1][1]) / 2

    @staticmethod
    def angle(shape: Line) -> Number:
        """
        Calculates the angle at (x0 + 1, y0), (x0, y0), (x1, y1)

        :param shape: The line who's angle is needed
        :return: The angle of the line (between -pi and pi)
        """
        return np.arctan2(shape[0][1] - shape[1][1], shape[0][0] - shape[1][0])

    @classmethod
    def angle_positive(cls, shape: Line) -> Number:
        """
        Calculates the angle at (x0 + 1, y0), (x0, y0), (x1, y1)
        Will always return a positive value

        :param shape: The line who's angle is needed
        :return: The angle of the line (between 0 and 2*pi)
        """
        angle = cls.angle(shape)
        if angle < 0:
            angle = 2 * np.pi + angle
        return angle

    @staticmethod
    def infinite_line_params(shape: Line) -> Point:
        """
        Calculates the parameters (m, b) such that the function y = m * x + b contains the entire given line

        :param shape: The line to find
        :return: A tuple of (m, b)
        """
        m = (shape[0][1] - shape[1][1]) / (shape[0][0] - shape[1][0])
        b = shape[0][1] - m * shape[0][0]
        return m, b

    @classmethod
    def collision(cls, shape1: Line, shape2: Line) -> bool:
        if almost_equal(shape1[0][0], shape1[1][0]):  # parallel to y
            if almost_equal(shape2[0][1], shape2[1][1]):  # parallel to x
                return min(shape2[0][0], shape2[1][0]) <= shape1[0][0] <= max(shape2[0][0], shape2[1][0]) and \
                       min(shape1[0][1], shape1[1][1]) <= shape2[0][1] <= max(shape1[0][1], shape1[1][1])
            else:  # inverse x and y
                shape1 = (shape1[0][1], -shape1[0][0]), (shape1[1][1], -shape1[1][0])
                shape2 = (shape2[0][1], -shape2[0][0]), (shape2[1][1], -shape2[1][0])
        if almost_equal(shape2[0][0], shape2[1][0]):  # parallel to y
            if almost_equal(shape1[0][1], shape1[1][1]):  # parallel to x
                return min(shape1[0][0], shape1[1][0]) <= shape2[0][0] <= max(shape1[0][0], shape1[1][0]) and \
                       min(shape2[0][1], shape2[1][1]) <= shape1[0][1] <= max(shape2[0][1], shape2[1][1])
            else:  # rotate by 90 deg
                shape1 = (shape1[0][1], -shape1[0][0]), (shape1[1][1], -shape1[1][0])
                shape2 = (shape2[0][1], -shape2[0][0]), (shape2[1][1], -shape2[1][0])

        m1, b1 = cls.infinite_line_params(shape1)
        m2, b2 = cls.infinite_line_params(shape2)
        if almost_equal(m1, m2):
            if not almost_equal(b1, b2):
                return False
            return min(shape1[0][0], shape1[1][0]) <= max(shape2[0][0], shape2[1][0]) <= max(shape1[0][0],
                                                                                             shape1[1][0]) or min(
                shape2[0][0], shape2[1][0]) <= max(shape1[0][0], shape1[1][0]) <= max(shape2[0][0], shape2[1][0])

        collision_x = (b1 - b2) / (m2 - m1)
        return min(shape1[0][0], shape1[1][0]) <= collision_x <= max(shape1[0][0], shape1[1][0]) and \
               min(shape2[0][0], shape2[1][0]) <= collision_x <= max(shape2[0][0], shape2[1][0])

    @classmethod
    def area(cls, shape: Line) -> Number:
        # A line has no area
        return 0
