import numpy as np

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
        :param contour_min_area: the minimal area of a contour, used in FilterContours
        """
        ObjectFinder.__init__(self, threshold_func, game_object)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               sort_contours +
                               contours_to_rotated_rects_sorted +
                               filter_inner_rotated_rects)
        self.area_scalar = area_scalar

    def __call__(self, frame, camera):
        rects = self._full_pipeline(frame)
        return list(map(
            lambda rect: self.game_object.location_by_params(camera,
                                                             self.area_scalar * np.sqrt(rect[1][0] * rect[1][1]),
                                                             rect[0]), rects))
        # d = []
        # for rect in rects:
        #    area = self.area_scalar * np.sqrt(rect[2] * rect[3])
        #    center = [(rect[0] + rect[2]) / 2, (rect[1] + rect[3]) / 2]
        #    d.append(self.im_object.location_by_params(camera, area, center))
        # return d
