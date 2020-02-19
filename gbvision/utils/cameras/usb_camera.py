from .camera import CameraData, Camera
from gbvision.models.cameras import UNKNOWN_CAMERA
import cv2
import platform
import sys
import subprocess


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

    @staticmethod
    def __is_on_linux() -> bool:
        return platform.system() == 'Linux'

    def __v4l2_ctl_command(self, cmd, value) -> int:
        try:
            return subprocess.call(['v4l2-ctl', '-d', f'/dev/video{self.port}', '-c', f'{cmd}={value}'])
        except FileNotFoundError:
            print(
                "[WARN] setting some parameters such as exposure may not on a Linux machine work if you do not have "
                "v4l2 installed, if the command you tried to run does not work please install v4l2 using 'sudo apt "
                "install v4l-utils'",
                file=sys.stderr)
            return -1

    def set_exposure(self, exposure) -> bool:
        if self.__is_on_linux():
            if type(exposure) is bool:
                _exposure = int(exposure) + 10
            else:
                _exposure = exposure
            code = self.__v4l2_ctl_command('exposure_absolute', _exposure)
            if code == 0:
                return True
        if type(exposure) is bool:
            return self.set(cv2.CAP_PROP_EXPOSURE, int(exposure))
        return self.set(cv2.CAP_PROP_EXPOSURE, exposure)

    def set_auto_exposure(self, auto) -> bool:
        if self.__is_on_linux():
            if type(auto) is bool:
                _auto = 3 if auto else 1
            else:
                _auto = auto
            code = self.__v4l2_ctl_command('exposure_auto', _auto)
            if code == 0:
                return True
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

    def get_fps(self):
        return self.get(cv2.CAP_PROP_FPS)

    def set_fps(self, fps):
        return self.set(cv2.CAP_PROP_FPS, fps)
