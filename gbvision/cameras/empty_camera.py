from typing import Tuple, Union

from .camera import Camera
from .camera_data import CameraData
from ..constants.types import Frame


class EmptyCamera(Camera):
    def __init__(self, data: CameraData, width: int, height: int):
        self.data = data
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
