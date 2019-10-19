import abc

import numpy as np
import cv2


class StreamReceiver(abc.ABC):
    """
    this is an abstract receiver that receives stream from a broadcast receiver
    this class should not be instanced but inherited from

    :param shape: optional, the shape (x, y) of the sent frame, when set to something other then (0, 0) it overrides
        the fx and fy parameters, when set to (0, 0) it is not used
    :param fx: ratio between width of the read frame to the width of the frame returned, default is 1 (same width)
    :param fy: ratio between height of the read frame to the height of the frame returned,
        default is 1 (same height)
    """

    def __init__(self, shape=(0, 0), fx: float = 1.0, fy: float = 1.0):
        """
        initializes a stream receiver
        
        """
        self.shape = shape
        self.fx = fx
        self.fy = fy

    @abc.abstractmethod
    def get_frame(self) -> np.ndarray:
        """
        reads a frame from the stream and returns in

        :returns: the frame read as a numpy array
        """
        pass

    def _prep_frame(self, frame):
        """
        prepares the frame to be returned and used
        resize and convert to bgr channeled image
        
        :param frame: the frame to be prepared
        :return: the frame after preparations
        """
        if frame is None:
            return frame
        if len(frame.shape) < 3:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        frame = cv2.resize(frame, self.shape, fx=self.fx, fy=self.fy)
        return frame
