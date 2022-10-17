import abc
import pickle
from typing import Optional

import cv2

from gbvision.constants.types import Frame, Coordinates
from gbvision.utils.readable import Readable


class StreamReceiver(Readable, abc.ABC):
    """
    this is an abstract receiver that receives stream from a broadcast receiver
    this class should not be instanced but inherited from

    :param shape: Optional. The shape (x, y) of the sent frame (None to use the given frame's shape)
    :param fx: Optional, The ratio between width of the read frame to the width of the frame returned (None for 1)
    :param fy: ratio between height of the read frame to the height of the frame returned (None for 1)
    :param convert_from_grayscale: Should this receiver convert grayscale images to BGR images (default True)
    """

    def __init__(self, shape: Optional[Coordinates] = None, fx: Optional[float] = None, fy: Optional[float] = None,
                 convert_from_grayscale: bool = True):
        self.shape = shape
        self.fx = fx
        self.fy = fy
        self.convert_from_grayscale = convert_from_grayscale
        self.__width = 0
        self.__height = 0

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
        if len(frame.shape) < 3 and self.convert_from_grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        if self.shape is not None:
            frame = cv2.resize(frame, self.shape)
        if self.fx is not None or self.fy is not None:
            frame = cv2.resize(frame, (0, 0), fx=self.fx or 1.0, fy=self.fy or 1.0)
        self.__height, self.__width = frame.shape[:2]
        return frame

    def get_width(self) -> int:
        if self.shape is not None:
            return self.shape[0]
        return self.__width

    def get_height(self) -> int:
        if self.shape is not None:
            return self.shape[1]
        return self.__height

    def set_width(self, width: int) -> None:
        self.shape = (width, self.get_height())

    def set_height(self, height: int) -> None:
        self.shape = (self.get_width(), height)
