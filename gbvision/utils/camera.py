from .camera_data import CameraData
from exceptions import AbstractMethodCallingException
import numpy as np


class Camera:

    def read(self, image=None) -> (bool, np.ndarray):
        raise AbstractMethodCallingException()

    def release(self):
        raise AbstractMethodCallingException()

    def is_opened(self) -> bool:
        raise AbstractMethodCallingException()

    def set_exposure(self, exposure: int or float or bool) -> bool:
        raise AbstractMethodCallingException()

    def set_auto_exposure(self, auto: int or float or bool) -> bool:
        raise AbstractMethodCallingException()

    @property
    def data(self) -> CameraData:
        raise AbstractMethodCallingException()

    @property
    def focal_length(self):
        return self.data.focal_length

    @property
    def fov(self):
        return self.data.fov

    @property
    def width(self):
        raise AbstractMethodCallingException()

    @property
    def height(self):
        raise AbstractMethodCallingException()

    def _set_width(self, width):
        """
        unsafe set width
        supposed to be overriden and only used by rescale, resize and set_frame size methods
        never to be used by the programmer, only by the api
        :param width: new width
        """
        raise AbstractMethodCallingException()

    def _set_height(self, height):
        """
        unsafe set height
        supposed to be overriden and only used by rescale, resize and set_frame size methods
        never to be used by the programmer, only by the api
        :param height: new height
        """
        raise AbstractMethodCallingException()

    def rescale(self, factor: float):
        self._set_width(self.width * factor)
        self._set_height(self.height * factor)
        self.data.focal_length *= factor

    def resize(self, fx, fy):
        self._set_width(self.width * fx)
        self._set_height(self.height * fy)
        self.data.focal_length *= np.sqrt(fx*fy)

    def set_frame_size(self, width, height):
        old_width, old_height = self.width, self.height
        self._set_height(height)
        self._set_width(width)
        self.data.focal_length *= np.sqrt(width*height / (old_width*old_height))
