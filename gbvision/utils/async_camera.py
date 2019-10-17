import abc
from threading import Thread
from typing import Tuple

import numpy as np
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
    def _async_read(self) -> Tuple[bool, np.ndarray]:
        """
        reads asynchronously from the camera
        :return: tuple of bool (indicates if read was successful) and the frame (if successful, else None)
        """
        pass

    def __async_read_wrapper(self):
        while self.is_opened():
            self.__ok, self.__frame = self._async_read()

    @staticmethod
    def create_type(camera_class) -> type:
        """
        creates a new class that is similar to the given class, but has the async feature
        the constructor of the new class is the same as the given class, but adds a new parameter at the beginning
        the first parameter to the new constructor is a stream broadcaster
        :param camera_class: the class to wrap
        :return: the wrapped class as a type that can be instanced
        """

        class _AsyncCamera(AsyncCamera, camera_class):
            def _async_read(self):
                return camera_class.read(self)

            def __init__(self, *args, **kwargs):
                camera_class.__init__(self, *args, **kwargs)
                AsyncCamera.__init__(self)

        return _AsyncCamera
