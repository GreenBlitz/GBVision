from typing import Tuple

from gbvision.constants.types import Frame
from .stream_camera import SimpleStreamCamera
from gbvision.models.cameras import UNKNOWN_CAMERA
from .usb_camera import USBCamera


class USBStreamCamera(SimpleStreamCamera, USBCamera):
    """
    a simple USB stream camera
    """

    def _read(self) -> Tuple[bool, Frame]:
        return USBCamera.read(self)

    def __init__(self, broadcaster, port, should_stream=False, data=UNKNOWN_CAMERA):
        SimpleStreamCamera.__init__(self, broadcaster, should_stream=should_stream)
        USBCamera.__init__(self, port, data)
