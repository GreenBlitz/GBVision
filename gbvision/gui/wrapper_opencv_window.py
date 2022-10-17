from abc import ABC

import cv2

from gbvision.models.system import EMPTY_PIPELINE
from .opencv_window import OpenCVWindow
from .wrapper_window import WrapperWindow
from gbvision.constants.types import Frame, ROI


class WrapperOpenCVWindow(OpenCVWindow, WrapperWindow, ABC):
    """
    A basic window that displays a feed from a camera

    :param wrap_object: The object from which to read the frame
    :param drawing_pipeline: Optional. A pipeline of drawing functions that will run on the frame before displaying it
    :param exit_button: An array of keys (a string), when one of the keys are pressed the window will be closed
    :param window_name: The title of the window
    """

    def __init__(self, window_name: str, wrap_object, exit_button='qQ', drawing_pipeline=EMPTY_PIPELINE,
                 flags=cv2.WINDOW_FREERATIO):
        OpenCVWindow.__init__(self, window_name, flags=flags, exit_button=exit_button)
        WrapperWindow.__init__(self, window_name=window_name, wrap_object=wrap_object,
                               drawing_pipeline=drawing_pipeline)

    def show_async(self) -> None:
        self.flags = cv2.WINDOW_AUTOSIZE
        WrapperWindow.show_async(self)

    def select_roi(self, frame: Frame = None) -> ROI:
        if frame is None:
            frame = self._get_frame()
        return OpenCVWindow.select_roi(self, frame)
