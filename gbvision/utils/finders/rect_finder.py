from typing import List

from gbvision.constants.types import Frame, Rect, FilterFunction

from .object_finder import ObjectFinder
from gbvision.models.contours import find_contours, contours_to_rects, FilterContours
from gbvision.models.system import EMPTY_PIPELINE

from gbvision.utils.shapes.base_rect import BaseRect


class RectFinder(ObjectFinder):
    """
    finds a rectangular shaped object

    :param area_scalar: optional, a scalar to multiply the area by, for fine tuning of the function's output
    :param contour_min_area: the minimal area of a contour, used for FilterContours, default is 0 (no area limit)
    :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
     the finder is searching, the object needs to be white and the rest if the image black (doesn't
     have to be perfect)
    :param contours_process: a pipeline to run on the list of contours (optional)
    :param rects_process: a pipeline to run on the list of rects (optional)
    """

    @staticmethod
    def _base_shape():
        return BaseRect

    def __init__(self, threshold_func: FilterFunction, game_object, area_scalar=1.0, contour_min_area=0.0,
                 contours_process=EMPTY_PIPELINE, rects_process=EMPTY_PIPELINE):
        ObjectFinder.__init__(self, game_object, area_scalar=area_scalar)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               contours_process +
                               contours_to_rects +
                               rects_process)

    def find_shapes_unsorted(self, frame: Frame) -> List[Rect]:
        return self._full_pipeline(frame)
