import numpy as np

from gbvision.exceptions import AbstractMethodCallingException


class StreamReceiver:
    """
    this is an abstract receiver that receives stream from a broadcast receiver
    this class should not be instanced but inherited from
    """

    def __init__(self, fx: float = 1.0, fy: float = 1.0):
        """
        initializes a stream receiver
        :param fx: ratio between width of the read frame to the width of the frame returned, default is 1 (same width)
        :param fy: ratio between height of the read frame to the height of the frame returned,
         default is 1 (same height)
        """
        self.fx = fx
        self.fy = fy

    def get_frame(self) -> np.ndarray:
        """
        reads a frame from the stream and returns in
        :returns: the frame read as a numpy array
        """
        raise AbstractMethodCallingException()
