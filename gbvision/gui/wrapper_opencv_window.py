from abc import ABC

import cv2

from gbvision.models.system import EMPTY_PIPELINE
from .opencv_window import OpenCVWindow
from .wrapper_window import WrapperWindow


class WrapperOpenCVWindow(OpenCVWindow, WrapperWindow, ABC):
    """
    a basic window that displays a feed from a camera

    :param wrap_object: the object from which to read the frame
    :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
    :param exit_button: an array of keys (a string), when one of the keys are pressed the window will be closed
    :param window_name: the title of the window
    """

    def __init__(self, window_name: str, wrap_object, exit_button='qQ', drawing_pipeline=EMPTY_PIPELINE,
                 flags=cv2.WINDOW_FREERATIO):
        """
        initializes the stream window
        
        """
        OpenCVWindow.__init__(self, window_name, flags=flags, exit_button=exit_button)
        WrapperWindow.__init__(self, window_name=window_name, wrap_object=wrap_object,
                               drawing_pipeline=drawing_pipeline)

    def show_async(self):
        self.flags = cv2.WINDOW_AUTOSIZE
        self.open()
        WrapperWindow.show_async(self)
