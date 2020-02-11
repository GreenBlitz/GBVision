from abc import ABC

from .window import Window
import cv2
from gbvision.models.system import EMPTY_PIPELINE


class OpenCVWindow(Window, ABC):
    """
    a basic window that uses the opencv gui module

    :param exit_button: a list of chars (or string) that will close the window when pressed
    :param flags: opencv window flags (default is WINDOW_FREERATIO)
    """

    def __init__(self, window_name: str, exit_button='qQ', drawing_pipeline=EMPTY_PIPELINE, flags=cv2.WINDOW_FREERATIO):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.exit_button = exit_button
        self.flags = flags
        self.last_key_pressed = None

    def _show_frame(self, frame):
        if frame is None:
            return False
        cv2.imshow(self.window_name, frame)
        k = chr(cv2.waitKey(1) & 0xFF)
        self.last_key_pressed = k
        if k in self.exit_button:
            return False
        return True

    def _open(self):
        cv2.namedWindow(self.window_name, self.flags)

    def _close(self):
        cv2.destroyWindow(self.window_name)
