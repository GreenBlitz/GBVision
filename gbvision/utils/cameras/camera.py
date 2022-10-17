import abc
from typing import Union

import numpy as np

from gbvision.constants.types import Number
from gbvision.utils.readable import Readable
from .camera_data import CameraData


class Camera(Readable, abc.ABC):
    """
    An abstract class representing a camera
    """

    @abc.abstractmethod
    def is_opened(self) -> bool:
        """
        Checks if the camera can be read from

        :return: True if the camera can be read from, otherwise False
        """

    @abc.abstractmethod
    def set_exposure(self, exposure: Union[int, float, bool]) -> bool:
        """
        Sets the camera's exposure

        :param exposure: the new exposure
        :return: True on success, False on failure
        """

    @abc.abstractmethod
    def set_auto_exposure(self, auto: Union[int, float, bool]) -> bool:
        """
        Sets the camera's auto exposure

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
        :return: The width of a frame read from this camera
        """

    @abc.abstractmethod
    def get_height(self) -> int:
        """
        :return: The height of a frame read from this camera
        """

    @abc.abstractmethod
    def _set_width(self, width: int) -> None:
        """
        Snsafe set width
        Only used by rescale, resize and set_frame size methods
        Never to be used by the programmer, only by the API

        :param width: new width
        """

    @abc.abstractmethod
    def _set_height(self, height: int) -> None:
        """
        Unsafe set height
        Only used by rescale, resize and set_frame size methods
        Never to be used by the programmer, only by the API

        :param height: new height
        """

    @abc.abstractmethod
    def get_fps(self) -> Number:
        """
        Gets the fps of this camera

        :return: The fps of the camera
        """

    @abc.abstractmethod
    def set_fps(self, fps: Number) -> bool:
        """
        Sets the fps for this camera

        :return: True on success, False otherwise
        """

    def rescale(self, factor: float) -> None:
        """
        Rescale the size of the frames read from this camera by a factor

        :param factor: The rescaling factor
        """
        self._set_width(int(self.get_width() * factor))
        self._set_height(int(self.get_height() * factor))
        self.get_data().focal_length *= factor

    def resize(self, fx: float, fy: float) -> None:
        """
        Rescale the size of the frames read from this camera by different width and height factors

        :param fx: The width factor
        :param fy: The height factor
        """
        self._set_width(int(self.get_width() * fx))
        self._set_height(int(self.get_height() * fy))
        self.get_data().focal_length *= np.sqrt(fx * fy)

    def set_frame_size(self, width: int, height: int) -> None:
        """
        Reset the width and height of frames read from this camera to given values
        
        :param width: The new width
        :param height: The new height
        """
        old_width, old_height = self.get_width(), self.get_height()
        self._set_height(height)
        self._set_width(width)
        self.get_data().focal_length *= np.sqrt(width * height / (old_width * old_height))
