from abc import ABC

from .window import Window
import cv2
from gbvision.models.system import EMPTY_PIPELINE
from gbvision.constants.types import ROI, Frame


class OpenCVWindow(Window, ABC):
    """
    A basic window that uses the opencv gui module

    :param exit_button: A list of chars (or string) that will close the window when pressed
    :param flags: OpenCV window flags (default is WINDOW_FREERATIO)
    """

    def __init__(self, window_name: str, exit_button='qQ', drawing_pipeline=EMPTY_PIPELINE, flags=cv2.WINDOW_FREERATIO):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.exit_button = exit_button
        self.flags = flags
        self.last_key_pressed = None

    def _show_frame(self, frame: Frame) -> bool:
        if frame is None:
            return False
        cv2.imshow(self.window_name, frame)
        k = chr(cv2.waitKey(1) & 0xFF)
        self.last_key_pressed = k
        if k in self.exit_button:
            return False
        return True

    def _open(self) -> None:
        cv2.namedWindow(self.window_name, self.flags)

    def _release(self) -> None:
        cv2.destroyWindow(self.window_name)

    def select_roi(self, frame: Frame) -> ROI:
        """
        Presents this frame on the window, and allows the user to select a rectangular area from the frame

        :param frame: The frame to show
        :return: The selected rectangular area, as a gbvision.ROI (similar to gbvision.Rect but all values are integers)
        """
        return cv2.selectROI(self.window_name, frame)
