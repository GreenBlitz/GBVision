from gbvision.constants.types import *
from gbvision.continuity.continues_shape import ContinuesShape
from gbvision.utils.tracker import Tracker


# TODO add docs

class ContinuesRect(ContinuesShape):
    def __init__(self, rect: Rect, tracker=None, max_area_ratio=2.0, max_distance_ratio=0.1):
        assert max_area_ratio > 1.0
        self._rect = rect
        self._count = 0
        self._tracker = Tracker() if tracker is None else tracker
        self.max_area_ratio = max_area_ratio
        self.max_distance_ratio = max_distance_ratio

    def _shape_collision(self, shape) -> bool:
        return not(self._shape[0] > shape[0] + shape[2] or
                   shape[0] > self._shape[0] + self._shape[2] or
                   self._shape[1] > shape[1] + shape[3] or
                   shape[1] > self._shape[1] + self._shape[3])

    @staticmethod
    def _shape_area(rect: Rect) -> Number:
        return rect[2] * rect[3]

    @staticmethod
    def _from_bounding_rect(bounding_rect: Rect):
        return bounding_rect

    @staticmethod
    def _to_bounding_rect(rect: Rect) -> Rect:
        return rect

    @staticmethod
    def __rect_area(rect):
        return rect[2] * rect[3]

    @staticmethod
    def _shape_square_distance(self, rect: Rect) -> Number:
        return (self._get_center(rect)[0] - self._shape)**2 + (self._get_center(rect)[1] - self._shape[1])**2

    @staticmethod
    def _get_center(rect: Rect) -> Point:
        center_x = (rect[0] + rect[3])/2
        center_y = (rect[1] + rect[4])/2
        return [center_x, center_y]

