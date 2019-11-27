from typing import List

from gbvision.constants.types import Frame, Rect

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
        ObjectFinder.__init__(self, threshold_func, game_object)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               sort_contours +
                               contours_to_rects_sorted +
                               filter_inner_rects)
        self.area_scalar = area_scalar

    def __call__(self, frame, camera):
        rects = self._full_pipeline(frame)
        return list(map(
            lambda rect: self.game_object.location_by_params(camera, self.area_scalar * np.sqrt(rect[2] * rect[3]),
                                                             [(rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2]),
            rects))

    def get_shape(self, frame: Frame) -> List[Rect]:
        return self._full_pipeline(frame)
