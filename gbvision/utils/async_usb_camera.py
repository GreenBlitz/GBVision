from threading import Thread, main_thread
from .usb_camera import USBCamera


class AsyncUSBCamera(USBCamera):
    """
    a usb camera class that reads from the device on another thread
    use this when multiple threads are trying to read from the camera at once
    """
    def __init__(self, port, data):
        USBCamera.__init__(self, port, data)
        self._ok, self._frame = False, None
        self._thread = Thread(target=self._async_camera_read)
        self._thread.start()

    def read(self, image=None):
        return self._ok, self._frame

    def _async_camera_read(self):
        while self.is_opened() and main_thread().is_alive():
            self._ok, self._frame = USBCamera.read(self)
