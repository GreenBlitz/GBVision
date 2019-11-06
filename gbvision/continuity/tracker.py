import cv2

class __EmptyTracker:
        def __init__(self):
            self.__rect = None
        
        def init(self, '''frame - not using it, no need''', rect):
            self.__rect = rect
            return True

        def update(self, frame):
            return True, self.__rect



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


class Tracker:
    """
    tracker that tracks rectangle in frame

    :param tracker_type: Tracker algorithm taken from this list: BOOSTING, MIL, KCF, TLD, MEDIANFLOW
        GOTURN, MOSSE, CSRT, EMPTY. (Default is BOOSTING)
    """

    def __init__(self, tracker_type = "BOOSTING"):
        assert tracker_type.upper() in TRACKER_ALGORITHMS
        tracker_type = tracker_type.upper()
        self.tracker = TRACKER_ALGORITHMS[tracker_type]()
        self.tracker_type = tracker_type

    def init(self, frame, rect):
        """
        Initlize the tracker

        :param frame: The frame
        :param rect: Given rectangle
        :return: True if initialization went succesfully, false otherwise
        """
        return self.tracker.init(frame,tuple([max(x,0) for x in rect]))
    
    def get_rect(self, frame):
        """
        Get the rect location in new frame

        :param frame: the frame
        :return: The location of the rect in new frame

        """
        return [int(x) for x in self.tracker.update(frame)[1]]
