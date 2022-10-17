from typing import Tuple

from gbvision.constants.types import Frame
from .streaming_camera import SimpleStreamingCamera
from gbvision.models.cameras import UNKNOWN_CAMERA
from .usb_camera import USBCamera


class USBStreamingCamera(SimpleStreamingCamera, USBCamera):
    """
    A simple USB stream camera
    """

    def release(self) -> None:
        USBCamera.release(self)
        self.stream_broadcaster.release()

    def _read(self) -> Tuple[bool, Frame]:
        return USBCamera.read(self)

    def __init__(self, broadcaster, port, should_stream=False, data=UNKNOWN_CAMERA):
        SimpleStreamingCamera.__init__(self, broadcaster, should_stream=should_stream)
        USBCamera.__init__(self, port, data)
