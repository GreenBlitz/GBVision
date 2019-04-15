from .object_finder import ObjectFinder
from models import *


class PolygonFinder(ObjectFinder):
    def __init__(self, threshold_func, game_object, area_scalar=1.0, contour_min_area=3.0):
        ObjectFinder.__init__(self, threshold_func, game_object)
        self._full_pipeline = (threshold_func +
                               find_contours +
                               filter_contours(min_area=contour_min_area) +
                               sort_contours)
        self.area_scalar = area_scalar

    def __call__(self, frame, camera):
        contours = self._full_pipeline(frame)
        return map(
            lambda cnt: self.game_object.location3d_by_params(camera, self.area_scalar * np.sqrt(cv2.contourArea(cnt)),
                                                            contour_center(cnt)), contours)
