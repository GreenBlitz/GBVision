from .camera import CameraData, Camera
from gbvision.constants.cameras import UNKNOWN_CAMERA
import cv2


class USBCamera(cv2.VideoCapture, Camera):
    """
    a basic usb connected camera which inherits from cv2 VideoCapture

    :param port: the usb port to which the camera is connected
    :param data: the camera data object that describes this camera
    """

    def __init__(self, port: int, data: CameraData = UNKNOWN_CAMERA):
        """
        initializes the camera
        
        """
        cv2.VideoCapture.__init__(self, port)
        self._data = data.copy()
        self.port = port

    def is_opened(self) -> bool:
        return self.isOpened()

    def set_exposure(self, exposure) -> bool:
        if type(exposure) is bool:
            return self.set(cv2.CAP_PROP_EXPOSURE, int(exposure))
        return self.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def set_auto_exposure(self, auto) -> bool:
        if type(auto) is bool:
            return self.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75 if auto else 0.25)
        return self.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto)

    def get_data(self):
        return self._data

    def get_width(self):
        return self.get(cv2.CAP_PROP_FRAME_WIDTH)

    def get_height(self):
        return self.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def _set_width(self, width):
        return self.set(cv2.CAP_PROP_FRAME_WIDTH, width)

    def _set_height(self, height):
        return self.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
