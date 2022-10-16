from typing import Tuple, Union

from .camera import Camera
from .camera_data import CameraData
from gbvision.constants.types import Frame
from gbvision.utils.net.stream_receiver import StreamReceiver


class StreamCamera(Camera):
    """
    A camera class which receives it's frames from a stream receiver

    :param data: The camera's CameraData object, should match the remote camera's data
    :param stream_receiver: The stream receiver to use
    """

    def __init__(self, data: CameraData, stream_receiver: StreamReceiver):
        self.__data = data.copy()
        self.stream_receiver = stream_receiver

    def release(self):
        self.stream_receiver.release()

    def is_opened(self) -> bool:
        return self.stream_receiver.is_opened()

    def set_exposure(self, exposure: Union[int, float, bool]) -> bool:
        return False

    def set_auto_exposure(self, auto: Union[int, float, bool]) -> bool:
        return False

    def get_data(self) -> CameraData:
        return self.__data

    def get_width(self) -> int:
        return self.stream_receiver.get_width()

    def get_height(self) -> int:
        return self.stream_receiver.get_height()

    def _set_width(self, width: int):
        self.stream_receiver.set_width(width)

    def _set_height(self, height: int):
        self.stream_receiver.set_height(height)

    def read(self) -> Tuple[bool, Frame]:
        return self.stream_receiver.read()

    def get_fps(self):
        return -1

    def set_fps(self, fps):
        return False
