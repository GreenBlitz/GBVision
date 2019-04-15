from constants import SQRT_PI
from models import find_contours, filter_contours, contours_to_circles_sorted, filter_inner_circles
from .object_finder import ObjectFinder


class CircleFinder(ObjectFinder):
    def __init__(self, threshold_func, game_object):
        ObjectFinder.__init__(self, threshold_func, game_object)
        self._full_pipeline = (threshold_func +
                               find_contours +
                               filter_contours +
                               contours_to_circles_sorted +
                               filter_inner_circles)

    def __call__(self, frame, camera):
        circles = self._full_pipeline(frame)
        return map(lambda circ: self.game_object.location3d_by_params(camera, SQRT_PI * circ[1], circ[0]), circles)
