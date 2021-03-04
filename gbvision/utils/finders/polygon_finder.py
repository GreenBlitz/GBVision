from typing import List

from gbvision.models.system import EMPTY_PIPELINE
from gbvision.constants.types import Frame, Polygon, FilterFunction
from gbvision.models.contours import FilterContours, find_contours, contours_to_polygons
from .object_finder import ObjectFinder
from gbvision.utils.shapes.base_polygon import BasePolygon


class PolygonFinder(ObjectFinder):
    """
    finds any generic polygon, not recommended when another finder can be used

    :param area_scalar: optional, a scalar to multiply the area by, for fine tuning of the function's output
    :param contour_min_area: the minimal area of a contour, used for FilterContours, default is 0 (no area limit)
    :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
     the finder is searching, the object needs to be white and the rest if the image black (doesn't
     have to be perfect)
    :param contours_process: a pipeline to run on the list of contours (optional)
    :param polygons_process: a pipeline to run on the list of polygons (optional)
    """

    @staticmethod
    def _base_shape():
        return BasePolygon

    def __init__(self, threshold_func: FilterFunction, game_object, area_scalar=1.0, contour_min_area=0.0,
                 contours_process=EMPTY_PIPELINE, polygons_process=EMPTY_PIPELINE):
        ObjectFinder.__init__(self, game_object, area_scalar=area_scalar)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               contours_process +
                               contours_to_polygons +
                               polygons_process)

    def find_shapes_unsorted(self, frame: Frame) -> List[Polygon]:
        return self._full_pipeline(frame)
