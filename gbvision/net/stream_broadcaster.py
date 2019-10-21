import abc

import cv2
import time

from gbvision.constants.types import Frame


class StreamBroadcaster(abc.ABC):
    """
    this is an abstract broadcaster that sends stream to a broadcast receiver
    this class should not be instanced but inherited from
    creates a new stream broadcaster with all parameters that are used in every broadcaster
    
    :param shape: optional, the shape (x, y) of the sent frame, when set to something other then (0, 0) it overrides
        the fx and fy parameters, when set to (0, 0) it is not used
    :param fx: ratio between width of the given frame to the width of the frame sent, default is 1 (same width)
    :param fy: ratio between height of the given frame to the height of the frame sent, default is 1 (same height)
    :param use_grayscale: boolean indicating if the frame should be converted to grayscale when sent,
        default is False
    :param max_fps: integer representing the maximum fps (frames per second) of the stream, when set to None
        there is no fps limitation, default is None
    """

    def __init__(self, shape=(0, 0), fx: float = 1.0, fy: float = 1.0, use_grayscale: bool = False,
                 max_fps: int = None):
        self.shape = shape
        self.fx = fx
        self.fy = fy
        self.use_grayscale = use_grayscale
        self.max_fps = max_fps
        self.prev_time = 0.0

    @abc.abstractmethod
    def send_frame(self, frame: Frame):
        """
        sends the given frame to the stream receiver
        :param frame: the frame to send
        """
        pass

    def _prep_frame(self, frame):
        """
        prepares an image to be sent
        resize and convert the colors of the image by the parameters of the stream broadcaster
        :param frame: the frame to prepare
        :return: the frame after preparation
        """
        frame = cv2.resize(frame, self.shape, fx=self.fx, fy=self.fy)
        if self.use_grayscale and len(frame.shape) > 2:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def _legal_time(self) -> bool:
        """
        checks if at the fps will not pass the max fps limit if an image will be sent at the current moment
        :return: true if the image can be sent, false otherwise
        """
        return self.max_fps is None or (time.time() - self.prev_time) * self.max_fps >= 1

    def _update_time(self):
        """
        updates the previous time a frame was sent, used at the end of send_frame
        """
        self.prev_time = time.time()
