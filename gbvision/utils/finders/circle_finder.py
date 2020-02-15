from typing import List

from gbvision.constants.types import Circle, Frame, FilterFunction

from gbvision.models.system import EMPTY_PIPELINE
from gbvision.models.contours import find_contours, FilterContours, contours_to_circles
from .object_finder import ObjectFinder
from gbvision.utils.shapes.base_circle import BaseCircle


class CircleFinder(ObjectFinder):
    """
    finds specific circular shaped object, and performs distance transformation

    :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
     the finder is searching, the object needs to be white and the rest if the image black (doesn't
     have to be perfect)
    :param contour_min_area: the minimal area of a contour, used for FilterContours, default is 0 (no area limit)
    :param contours_process: a pipeline to run on the list of contours (optional)
    :param circles_process: a pipeline to run on the list of circles (optional)
    """

    @staticmethod
    def _base_shape():
        return BaseCircle

    def __init__(self, threshold_func: FilterFunction, game_object, area_scalar=1.0, contour_min_area=0,
                 contours_process=EMPTY_PIPELINE, circles_process=EMPTY_PIPELINE):
        ObjectFinder.__init__(self, game_object, area_scalar=area_scalar)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               contours_process +
                               contours_to_circles +
                               circles_process)

    def find_shapes_unsorted(self, frame: Frame) -> List[Circle]:
        return self._full_pipeline(frame)

