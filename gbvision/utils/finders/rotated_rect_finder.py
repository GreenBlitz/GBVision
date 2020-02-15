from typing import List

from gbvision.constants.types import Frame, RotatedRect, FilterFunction

from gbvision.models.system import EMPTY_PIPELINE
from gbvision.models.contours import find_contours, FilterContours, contours_to_rotated_rects
from .object_finder import ObjectFinder
from gbvision.utils.shapes.base_rotated_rect import BaseRotatedRect


class RotatedRectFinder(ObjectFinder):
    """
    finds a rectangular object, but rotated. recommended to use when you know the shape isn't parallel to the camera

    :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
     the finder is searching, the object needs to be white and the rest if the image black (doesn't
     have to be perfect)
    :param area_scalar: optional, a scalar to multiply the area by, for fine tuning of the function's output
    :param contour_min_area: the minimal area of a contour, used for FilterContours, default is 0 (no area limit)
    :param contours_process: a pipeline to run on the list of contours (optional)
    :param rotated_rects_process: a pipeline to run on the list of rotated rects (optional)
    """

    @staticmethod
    def _base_shape():
        return BaseRotatedRect

    def __init__(self, threshold_func: FilterFunction, game_object, area_scalar=1.0, contour_min_area=0.0,
                 contours_process=EMPTY_PIPELINE, rotated_rects_process=EMPTY_PIPELINE):
        ObjectFinder.__init__(self, game_object, area_scalar=area_scalar)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               contours_process +
                               contours_to_rotated_rects +
                               rotated_rects_process)

    def find_shapes_unsorted(self, frame: Frame) -> List[RotatedRect]:
        return self._full_pipeline(frame)
