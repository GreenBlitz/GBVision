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
        self.data = b''
        self.payload_size = struct.calcsize("I")

    @abc.abstractmethod
    def _receive(self) -> bytes:
        """
        reads bytes from the stream and returns them
        the amount of bytes read is the choice of the programmer
        for UDP / RAW formats, a large amount is recommended
        for TCP / TCP like formats, a small amount is recommended

        """
        pass

    def _get_frame_data(self) -> bytes:
        """

        :return:
        """
        while len(self.data) < self.payload_size:
            self.data += self._receive()
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("I", packed_msg_size)[0]
        while len(self.data) < msg_size:
            self.data += self._receive()
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        return frame_data

    def read(self):
        frame_data = self._get_frame_data()
        frame = pickle.loads(frame_data)
        if frame is None:
            return False, None
        frame = cv2.imdecode(frame, -1)
        return True, self._prep_frame(frame)

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
