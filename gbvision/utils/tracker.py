import typing
from typing import Callable, Tuple, Optional

import cv2

from gbvision.constants.types import Frame, Rect, TrackerType

_major_ver, _minor_ver, _subminor_ver = cv2.__version__.split('.')


class _EmptyTracker:
    def __init__(self):
        self.__rect = None

    def init(self, frame: Frame, rect: Rect):
        self.__rect = rect
        return True

    def update(self, frame: Frame) -> Tuple[bool, Rect]:
        return True, self.__rect


def _get_tracker_create(tracker_name: str) -> Optional[Callable[[], TrackerType]]:
    if tracker_name == 'EMPTY':
        return _EmptyTracker
    try:
        if int(_major_ver) < 4 and int(_minor_ver) < 3:
            return lambda: cv2.cv2.Tracker_create(tracker_name.upper())
        attr_full_name = f'Tracker{tracker_name}_create'
        if hasattr(cv2, attr_full_name):
            return cv2.__dict__[attr_full_name]
        return cv2.legacy.__dict__[attr_full_name]
    except AttributeError:
        return None


class Tracker:
    """
    A tracker object that tracks a rectangle in a video using an opencv tracking algorithm

    :param tracker_type: Tracker algorithm taken from this list: BOOSTING, MIL, KCF, TLD, MEDIANFLOW,
        GOTURN, MOSSE, CSRT, EMPTY. (Default is EMPTY)
    """

    TRACKER_TYPE_BOOSTING = 'BOOSTING'
    TRACKER_TYPE_MIL = 'MIL'
    TRACKER_TYPE_KCF = 'KCF'
    TRACKER_TYPE_TLD = 'TLD'
    TRACKER_TYPE_MEDIANFLOW = 'MEDIANFLOW'
    TRACKER_TYPE_GOTURN = 'GOTURN'
    TRACKER_TYPE_MOSSE = 'MOSSE'
    TRACKER_TYPE_CSRT = 'CSRT'
    TRACKER_TYPE_EMPTY = 'EMPTY'

    _TRACKER_ALGORITHMS = {
        tracker_name: _get_tracker_create(tracker_type)
        for tracker_name, tracker_type in
        [(TRACKER_TYPE_BOOSTING, 'Boosting'),
         (TRACKER_TYPE_MIL, 'MIL'),
         (TRACKER_TYPE_KCF, 'KCF'),
         (TRACKER_TYPE_TLD, 'TLD'),
         (TRACKER_TYPE_MEDIANFLOW, 'MedianFlow'),
         (TRACKER_TYPE_GOTURN, 'GOTURN'),
         (TRACKER_TYPE_MOSSE, 'MOSSE'),
         (TRACKER_TYPE_CSRT, 'CSRT'),
         (TRACKER_TYPE_EMPTY, 'EMPTY')]
    }

    def __init__(self, tracker_type: str = TRACKER_TYPE_EMPTY):
        tracker_type = tracker_type.upper()
        assert tracker_type in self._TRACKER_ALGORITHMS, f'Unknown tracker type: {tracker_type}'
        assert self._TRACKER_ALGORITHMS[tracker_type] is not None,\
            f'Your version of OpenCV has no support for tracker type {tracker_type}'
        self.tracker = self._TRACKER_ALGORITHMS[tracker_type]()
        self.tracker_type = tracker_type

    def init(self, frame: Frame, rect: Rect) -> bool:
        """
        Initialize the tracker

        :param frame: The frame
        :param rect: Given rectangle
        :return: True if initialization went successfully, False otherwise
        """
        return self.tracker.init(frame, typing.cast(Rect, tuple([int(max(x, 0)) for x in rect])))

    def update(self, frame: Frame) -> Rect:
        """
        Get the rect location in new frame

        :param frame: The frame
        :return: The location of the rect in new frame
        """
        return self.tracker.update(frame)[1]
