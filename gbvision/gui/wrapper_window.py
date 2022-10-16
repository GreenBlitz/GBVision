import abc
from typing import Any

from gbvision.constants.types import Frame
from .window import Window
from gbvision.models.system import EMPTY_PIPELINE
from threading import Thread


class WrapperWindow(Window, abc.ABC):
    """
    A window class that uses an object (wrap_object) and reads frames from it in to display it's feed

    :param wrap_object: An object to read frames from, can be of any type
    """

    def __init__(self, window_name: str, wrap_object: Any, drawing_pipeline=EMPTY_PIPELINE):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.wrap_object = wrap_object

    def show_and_get_frame(self) -> Frame:
        """
        Shows one frame and returns it

        :return: The frame if the window was not closed, None otherwise
        """
        frame = self._get_frame()
        if self.show_frame(frame):
            return frame
        return None

    def show(self):
        """
        Reads from the wrap object and shows the frame until the window is closed
        """
        while True:
            if self.show_and_get_frame() is None:
                return

    @abc.abstractmethod
    def _get_frame(self) -> Frame:
        """
        Unsafely reads a frame from the wrapped object and returns the read frame
        
        :return: The read frame
        """

    def show_async(self) -> None:
        """
        Opens the steam video window on another thread
        """
        # Close existing window to allow it to re-open on the new thread
        if self.is_opened():
            self.release()
        Thread(target=self.show).start()
