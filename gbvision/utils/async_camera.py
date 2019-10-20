import abc
from threading import Thread
from typing import Tuple

import numpy as np

from gbvision.constants.types import Frame
from .camera import Camera


class AsyncCamera(Camera, abc.ABC):
    """
    an abstract class that represents an async camera
    the async camera is similar to a regular camera, but executes the read actions on another thread
    thus not blocking the processing thread
    """

    def __init__(self):
        self.__ok, self.__frame = False, None
        self.__thread = Thread(target=self.__async_read_wrapper)
        self.__thread.start()

    def read(self, image=None):
        return self.__ok, self.__frame

    @abc.abstractmethod
    def _read(self) -> Tuple[bool, Frame]:
        """
        reads from the camera synchronously (similar to Camera.read), unsafe, not to use by the programmer
        :return: tuple of bool (indicates if read was successful) and the frame (if successful, else None)
        """
        pass

    def __async_read_wrapper(self):
        while self.is_opened():
            self.__ok, self.__frame = self._read()


class SimpleAsyncCamera(AsyncCamera, abc.ABC):
    """
    this class implements the features of the
    """
    def _read(self):
        return self.read()
