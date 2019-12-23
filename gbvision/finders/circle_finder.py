from typing import List

from gbvision.constants.types import Circle, Frame, Number, Point, FilterFunction

from gbvision.constants.math import SQRT_PI
from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.models.contours import find_contours, FilterContours, contours_to_circles_sorted
from gbvision.models.shapes import filter_inner_circles
from .object_finder import ObjectFinder


class CircleFinder(ObjectFinder):
    """
    finds specific circular shaped object, and performs distance transformation

    :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
     the finder is searching, the object needs to be white and the rest if the image black (doesn't
     have to be perfect)
    :param contour_min_area: the minimal area of a contour, used for FilterContours, default is 0 (no area limit)
    """

    def __init__(self, threshold_func: FilterFunction, game_object, area_scalar=1.0, contour_min_area=0):
        ObjectFinder.__init__(self, game_object, area_scalar=area_scalar)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               contours_to_circles_sorted +
                               filter_inner_circles)

    def find_shapes(self, frame: Frame) -> List[Circle]:
        return self._full_pipeline(frame)

    @staticmethod
    def _shape_root_area(shape: Circle) -> Number:
        return SQRT_PI * shape[1]

    @staticmethod
    def _shape_center(shape: Circle) -> Point:
        return shape[0]
