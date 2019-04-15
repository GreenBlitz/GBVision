from gbvision.exceptions import AbstractMethodCallingException


class StreamBroadcaster:
    """
    this is an abstract broadcaster that sends stream to a broadcast receiver
    this class should not be instanced but inherited from
    """

    def __init__(self, fx: float = 1.0, fy: float = 1.0, use_grayscale: bool = False, max_fps: int = None):
        """
        creates a new stream broadcaster with all parameters that are used in every broadcaster
        :param fx: ratio between width of the given frame to the width of the frame sent, default is 1 (same width)
        :param fy: ratio between height of the given frame to the height of the frame sent, default is 1 (same height)
        :param use_grayscale: boolean indicating if the frame should be converted to grayscale when sent,
         default is False
        :param max_fps: integer representing the maximum fps (frames per second) of the stream, when set to None
        there is no fps limitation, default is None
        """
        self.fx = fx
        self.fy = fy
        self.use_grayscale = use_grayscale
        self.max_fps = max_fps

    def send_frame(self, frame):
        """
        sends the given frame to the stream receiver
        :param frame: the frame to send
        """
        raise AbstractMethodCallingException()
