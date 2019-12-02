from typing import Tuple

from gbvision.constants.types import Frame
from .stream_camera import SimpleStreamCamera
from gbvision.constants.cameras import UNKNOWN_CAMERA
from .usb_camera import USBCamera


class USBStreamCamera(SimpleStreamCamera, USBCamera):
    """
    a simple USB stream camera
    """
    def _read(self) -> Tuple[bool, Frame]:
        return USBCamera.read(self)

    def __init__(self, broadcaster, port, data=UNKNOWN_CAMERA):
        SimpleStreamCamera.__init__(self, broadcaster)
        USBCamera.__init__(self, port, data)
