import abc
from typing import Union

import numpy as np
from gbvision.constants.types import Number

from .camera_data import CameraData
from gbvision.utils.readable import Readable


class Camera(Readable, abc.ABC):
    """
    an abstract class representing a camera
    """

    @abc.abstractmethod
    def release(self):
        """
        closes the handle to this camera, if it is not necessary please override this method to a blank method
        """

    @abc.abstractmethod
    def is_opened(self) -> bool:
        """
        checks if the camera can be read from

        :return: True if the camera can be read from, otherwise False
        """

    @abc.abstractmethod
    def set_exposure(self, exposure: Union[int, float, bool]) -> bool:
        """
        sets the camera's exposure

        :param exposure: the new exposure
        :return: True on success, False on failure
        """

    @abc.abstractmethod
    def set_auto_exposure(self, auto: Union[int, float, bool]) -> bool:
        """
        sets the camera's auto exposure

        :param auto: the new auto exposure
        :return: True on success, False on failure
        """

    @abc.abstractmethod
    def get_data(self) -> CameraData:
        """
        :return: this camera's constant descriptor (must be the real descriptor, can't be a copy) \
            when the values of this descriptor are changed, the values of the real camera descriptor must also change
        """

    @abc.abstractmethod
    def get_width(self) -> int:
        """
        :return: the width of a frame read from this camera
        """

    @abc.abstractmethod
    def get_height(self) -> int:
        """
        :return: the height of a frame read from this camera
        """

    @abc.abstractmethod
    def _set_width(self, width: int):
        """
        unsafe set width
        supposed to be overridden and only used by rescale, resize and set_frame size methods
        never to be used by the programmer, only by the api

        :param width: new width
        """

    @abc.abstractmethod
    def _set_height(self, height: int):
        """
        unsafe set height
        supposed to be overridden and only used by rescale, resize and set_frame size methods
        never to be used by the programmer, only by the api

        :param height: new height
        """

    @abc.abstractmethod
    def get_fps(self) -> Number:
        """
        gets the fps of this camera

        :return: the fps of the camera
        """

    @abc.abstractmethod
    def set_fps(self, fps: Number) -> bool:
        """
        sets the fps for this camera

        :return: True on success, False otherwise
        """

    def rescale(self, factor: float):
        """
        rescale the size of the frames read from this camera by a factor

        :param factor: the rescaling factor
        """
        self._set_width(int(self.get_width() * factor))
        self._set_height(int(self.get_height() * factor))
        self.get_data().focal_length *= factor

    def resize(self, fx: float, fy: float):
        """
        rescale the size of the frames read from this camera by different width and height factors

        :param fx: the width factor
        :param fy: the height factor
        """
        self._set_width(int(self.get_width() * fx))
        self._set_height(int(self.get_height() * fy))
        self.get_data().focal_length *= np.sqrt(fx * fy)

    def set_frame_size(self, width: int, height: int):
        """
        reset the width and height of frames read from this camera to given values
        
        :param width: the new width
        :param height: the new height
        """
        old_width, old_height = self.get_width(), self.get_height()
        self._set_height(height)
        self._set_width(width)
        self.get_data().focal_length *= np.sqrt(width * height / (old_width * old_height))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

