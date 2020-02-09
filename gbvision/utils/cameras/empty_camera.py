from typing import Tuple, Union

from .camera import Camera
from .camera_data import CameraData
from gbvision.constants.types import Frame


class EmptyCamera(Camera):
    """
    a camera class used for testing, it cannot be read from but can be used for location finding with finders and game\
     objects, also used for measuring of distances when using streams instead of cameras to read frames

    :param data: the camera's CameraData object, should match the fake camera's data
    :param width: the width of a frame read from the fake camera
    :param height: the height of a frame read from the fake camera
    """

    def __init__(self, data: CameraData, width: int, height: int):
        self.data = data.copy()
        self.width = width
        self.height = height

    def release(self):
        pass

    def is_opened(self) -> bool:
        return False

    def set_exposure(self, exposure: Union[int, float, bool]) -> bool:
        return False

    def set_auto_exposure(self, auto: Union[int, float, bool]) -> bool:
        return False

    def get_data(self) -> CameraData:
        return self.data

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height

    def _set_width(self, width: int):
        self.width = width

    def _set_height(self, height: int):
        self.height = height

    def read(self) -> Tuple[bool, Frame]:
        return False, None

    def get_fps(self):
        return 0

    def set_fps(self, fps):
        return False
