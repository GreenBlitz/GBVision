import abc
from typing import Union

import numpy as np

from gbvision.constants.types import Rect, Number, Frame
from gbvision.utils.tracker import Tracker


class ContinuesShape(abc.ABC):
    def __init__(self, shape, frame: Frame, tracker: Tracker = None, max_area_ratio=2.0, max_distance_ratio=0.1):
        assert max_area_ratio > 1.0
        self._shape = shape
        self._count = 0
        self._tracker = Tracker() if tracker is None else tracker
        self._tracker.init(frame, self._to_bounding_rect(shape))
        self.max_area_ratio = max_area_ratio
        self.max_distance_ratio = max_distance_ratio

    @abc.abstractmethod
    def _shape_collision(self, shape) -> bool:
        """
        """

    @staticmethod
    @abc.abstractmethod
    def _shape_area(shape) -> Number:
        """"

        """

    @abc.abstractmethod
    def _shape_square_distance(self, shape) -> Number:
        """

        """

    @staticmethod
    @abc.abstractmethod
    def _from_bounding_rect(bounding_rect: Rect):
        """

        """

    @staticmethod
    @abc.abstractmethod
    def _to_bounding_rect(shape) -> Rect:
        """

        """

    def _is_legal(self, shape):
        if self._shape_collision(shape):
            if 1.0 / self.max_area_ratio <= self._shape_area(self._shape) / self._shape_area(
                    shape) <= self.max_area_ratio:
                if self._shape_square_distance(shape) <= (
                        self._shape_area(self._shape) + self._shape_area(shape)) * self.max_distance_ratio:
                    return True
        return False

    def get(self):
        return self._shape

    def update(self, shape, frame: Frame) -> bool:
        if self._is_legal(shape):
            self._shape = shape
            self._count = 0
            self._tracker.init(frame, self._to_bounding_rect(shape))
            return True
        return False

    def update_forced(self, frame: Frame):
        self._shape = self._from_bounding_rect(self._tracker.update(frame))
        self._count += 1

    def is_lost(self, max_count: int):
        return max_count is not None and self._count <= max_count
