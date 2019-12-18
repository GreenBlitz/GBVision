from typing import List

from gbvision.constants.types import Frame, Rect, Number, Point

from .object_finder import ObjectFinder
from gbvision.models.contours import find_contours, FilterContours, sort_contours, contours_to_rects_sorted
from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.models.shapes import filter_inner_rects
import numpy as np


class RectFinder(ObjectFinder):
    """
    finds a rectangular shaped object
    """

    def __init__(self, threshold_func, game_object, area_scalar=1.0, contour_min_area=0):
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
                               contours_to_rects_sorted +
                               filter_inner_rects)

    def find_shapes(self, frame: Frame) -> List[Rect]:
        return self._full_pipeline(frame)

    @staticmethod
    def shape_root_area(shape: Rect) -> Number:
        return np.sqrt(shape[2] * shape[3])

    @staticmethod
    def shape_center(shape: Rect) -> Point:
        return (shape[0] + shape[2]) / 2, (shape[1] + shape[3]) / 2
