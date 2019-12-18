from typing import List

import numpy as np
from gbvision.constants.types import Frame, RotatedRect, Number, Point

from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.models.contours import find_contours, FilterContours, sort_contours, contours_to_rotated_rects_sorted
from gbvision.models.shapes import filter_inner_rotated_rects
from .object_finder import ObjectFinder


class RotatedRectFinder(ObjectFinder):
    """
    finds a rectangular object, but rotated. recommended to use when you know the shape isn't parallel to the camera
    """

    def __init__(self, threshold_func, game_object, area_scalar=1.0, contour_min_area=3.0):
        """

        :param area_scalar: optional, a scalar to multiply the area by, for fine tuning of the function's output
        :param contour_min_area: the minimal area of a contour, used for FilterContours, default is 0 (no area limit)
        """
        ObjectFinder.__init__(self, threshold_func, game_object, area_scalar=area_scalar)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               sort_contours +
                               contours_to_rotated_rects_sorted +
                               filter_inner_rotated_rects)

    def find_shapes(self, frame: Frame) -> List[RotatedRect]:
        return self._full_pipeline(frame)

    @staticmethod
    def _shape_root_area(shape: RotatedRect) -> Number:
        return np.sqrt(shape[1][0] * shape[1][1])

    @staticmethod
    def _shape_center(shape: RotatedRect) -> Point:
        return shape[0]