from constants import SQRT_PI
from models import find_contours, filter_contours, contours_to_circles_sorted, filter_inner_circles
from .object_finder import ObjectFinder


class CircleFinder(ObjectFinder):
    """
    finds a circular shaped object, like a ball or a disk
    """
    def __init__(self, threshold_func, game_object, contour_min_area=3.0):
        """
        initializes the finder
        :param contour_min_area: the minimal area of a contour, used in filter_contours
        """
        ObjectFinder.__init__(self, threshold_func, game_object)
        self._full_pipeline = (threshold_func +
                               find_contours +
                               filter_contours(min_area=contour_min_area) +
                               contours_to_circles_sorted +
                               filter_inner_circles)

    def __call__(self, frame, camera):
        circles = self._full_pipeline(frame)
        return map(lambda circ: self.game_object.location3d_by_params(camera, SQRT_PI * circ[1], circ[0]), circles)
