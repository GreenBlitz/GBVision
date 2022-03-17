import abc
import pickle
import cv2
import struct

from gbvision.constants.types import Frame
from gbvision.utils.readable import Readable


class StreamReceiver(Readable, abc.ABC):
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
        self.shape = shape
        self.fx = fx
        self.fy = fy

    @abc.abstractmethod
    def _get_bytes(self) -> bytes:
        """
        performs the entire process of reading from the socket
        any defragmentation and headers handling necessary needs to happen here

        :return: the bytes read from the socket, after defragmentation (if exists)
        """

    def read(self):
        frame_data = self._get_bytes()
        frame = self._from_bytes(frame_data)
        if frame is None:
            return False, None
        frame = cv2.imdecode(frame, -1)
        return True, self._prep_frame(frame)

    @staticmethod
    def _from_bytes(bytes_obj: bytes) -> object:
        """
        parses a binary represented object back to a python object

        :param bytes_obj: the binary output from the socket
        :return: a python object
        """
        return pickle.loads(bytes_obj)

    def _prep_frame(self, frame: Frame) -> Frame:
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
