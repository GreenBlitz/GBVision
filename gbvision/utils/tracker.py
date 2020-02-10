import cv2


class __EmptyTracker:
    def __init__(self):
        self.__rect = None

    def init(self, frame, rect):
        self.__rect = rect
        return True

    def update(self, frame):
        return True, self.__rect


try:
    TRACKER_ALGORITHMS = {
        "BOOSTING": cv2.TrackerBoosting_create,
        "MIL": cv2.TrackerMIL_create,
        "KCF": cv2.TrackerKCF_create,
        "TLD": cv2.TrackerTLD_create,
        "MEDIANFLOW": cv2.TrackerMedianFlow_create,
        "GOTURN": cv2.TrackerGOTURN_create,
        "MOSSE": cv2.TrackerMOSSE_create,
        "CSRT": cv2.TrackerCSRT_create,
        "EMPTY": __EmptyTracker
    }
except AttributeError:
    import sys
    print("[WARN] no trackers in your version of opencv, you may only use the empty tracker", file=sys.stderr)
    TRACKER_ALGORITHMS = {
        "EMPTY": __EmptyTracker
    }


class Tracker:
    """
    a tracker object that tracks a rectangle in a video using an opencv tracking algorithm

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

    def __init__(self, tracker_type="EMPTY"):
        tracker_type = tracker_type.upper()
        assert tracker_type in TRACKER_ALGORITHMS
        self.tracker = TRACKER_ALGORITHMS[tracker_type]()
        self.tracker_type = tracker_type

    def init(self, frame, rect):
        """
        Initlize the tracker

        :param frame: The frame
        :param rect: Given rectangle
        :return: True if initialization went succesfully, false otherwise
        """
        return self.tracker.init(frame, tuple([int(max(x, 0)) for x in rect]))

    def update(self, frame):
        """
        Get the rect location in new frame

        :param frame: the frame
        :return: The location of the rect in new frame

        """
        return self.tracker.update(frame)[1]
