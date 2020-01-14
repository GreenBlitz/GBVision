import abc
from threading import Thread
from typing import Tuple

import time

from gbvision.constants.types import Frame
from .camera import Camera


class AsyncCamera(Camera, abc.ABC):
    """
    an abstract class that represents an async camera
    the async camera is similar to a regular camera, but executes the read actions on another thread
    thus not blocking the processing thread

    you will usually want to inherit from this class and from another camera class in order to use the async functionality
    for example:

    Example::
        class AsyncUSBCamera(AsyncCamera, USBCamera):
            def _read(self) -> Tuple[bool, Frame]:
                return USBCamera.read(self)

            def __init__(self, port, data=UNKNOWN_CAMERA):
                USBCamera.__init__(self, port, data)
                AsyncCamera.__init__(self)
    """

    def __init__(self):
        self.__ok, self.__frame = False, None
        self.__thread = Thread(target=self.__async_read_wrapper)
        self.__thread.start()

    def read(self):
        return self.__ok, self.__frame

    def has_started_reading(self):
        return self.__frame is not None

    def wait_start_reading(self, wait_time=0.01):
        while not self.has_started_reading():
            time.sleep(wait_time)

    @abc.abstractmethod
    def _read(self) -> Tuple[bool, Frame]:
        """
        reads from the camera synchronously (similar to Camera.read), unsafe, not to use by the programmer
        this method will usually simply call super(self, CameraClass).read()
        
        :return: tuple of bool (indicates if read was successful) and the frame (if successful, else None)
        """

    def __async_read_wrapper(self):
        while self.is_opened():
            self.__ok, self.__frame = self._read()
