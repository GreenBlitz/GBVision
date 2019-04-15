import numpy as np

from gbvision.exceptions import AbstractMethodCallingException
from .camera_data import CameraData


class Camera:
    """
    an abstract class representing a camera
    """

    def read(self, image: np.ndarray = None) -> (bool, np.ndarray):
        """
        reads from the camera and returns a tuple of a boolean and the frame
        :param image: if not None, the frame will be read to this ndarray
        :return: a boolean indicating if the action was successful, and the frame if read was successful, otherwise None
        """
        raise AbstractMethodCallingException()

    def release(self):
        """
        closes the handle to this camera, if it is not necessary please override this method to a black method
        """
        raise AbstractMethodCallingException()

    def is_opened(self) -> bool:
        """
        checks if the camera can be read from
        :return: True if the camera can be read from, otherwise False
        """
        raise AbstractMethodCallingException()

    def set_exposure(self, exposure: int or float or bool) -> bool:
        """
        sets the camera's exposure
        :param exposure: the new exposure
        :return: True on success, False on failure
        """
        raise AbstractMethodCallingException()

    def set_auto_exposure(self, auto: int or float or bool) -> bool:
        """
        sets the camera's auto exposure
        :param auto: the new auto exposure
        :return: True on success, False on failure
        """
        raise AbstractMethodCallingException()

    @property
    def data(self) -> CameraData:
        """
        :return: this camera's constant descriptor (must be the real descriptor, can't be a copy)
        """
        raise AbstractMethodCallingException()

    @property
    def focal_length(self):
        """
        :return: this camera's focal length at the current moment
        """
        return self.data.focal_length

    @property
    def fov(self):
        """
        :return: this cameras field of view angle in radians
        """
        return self.data.fov

    @property
    def width(self):
        """
        :return: the width of a frame read from this camera
        """
        raise AbstractMethodCallingException()

    @property
    def height(self):
        """
        :return: the height of a frame read from this camera
        """
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
        """
        rescale the size of the frames read from this camera by a factor
        :param factor: the rescaling factor
        """
        self._set_width(self.width * factor)
        self._set_height(self.height * factor)
        self.data.focal_length *= factor

    def resize(self, fx, fy):
        """
        rescale the size of the frames read from this camera by different width and height factors
        :param fx: the width factor
        :param fy: the height factor
        """
        self._set_width(self.width * fx)
        self._set_height(self.height * fy)
        self.data.focal_length *= np.sqrt(fx * fy)

    def set_frame_size(self, width, height):
        """
        reset the width and height of frames read from this camera to given values
        :param width: the new width
        :param height: the new height
        """
        old_width, old_height = self.width, self.height
        self._set_height(height)
        self._set_width(width)
        self.data.focal_length *= np.sqrt(width * height / (old_width * old_height))
