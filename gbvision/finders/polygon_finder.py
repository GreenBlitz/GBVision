from typing import List

import cv2
import numpy as np

from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.constants.types import Frame, Polygon
from gbvision.models.contours import FilterContours, find_contours, sort_polygons, contour_center, contours_to_polygons
from .object_finder import ObjectFinder


class PolygonFinder(ObjectFinder):
    """
    finds any generic polygon, not recommended when another finder can be used
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
                               contours_to_polygons +
                               sort_polygons)
        self.area_scalar = area_scalar

    def __call__(self, frame, camera):
        contours = self._full_pipeline(frame)
        return list(map(
            lambda cnt: self.game_object.location_by_params(camera, self.area_scalar * np.sqrt(cv2.contourArea(cnt)),
                                                            contour_center(cnt)), contours))

    def get_shape(self, frame: Frame) -> List[Polygon]:
        return self._full_pipeline(frame)
