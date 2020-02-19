from typing import Tuple

from gbvision.constants.types import Frame
from .usb_camera import USBCamera
from .async_camera import AsyncCamera
from gbvision.models.cameras import UNKNOWN_CAMERA


class AsyncUSBCamera(AsyncCamera, USBCamera):
    """
    A simple async usb camera
    """

    def _read(self) -> Tuple[bool, Frame]:
        return USBCamera.read(self)

    def __init__(self, port, data=UNKNOWN_CAMERA):
        USBCamera.__init__(self, port, data)
        AsyncCamera.__init__(self)
