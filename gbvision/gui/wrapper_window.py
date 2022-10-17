import abc
from typing import Any, Tuple

from gbvision.constants.types import Frame
from .window import Window
from gbvision.models.system import EMPTY_PIPELINE
from threading import Thread

from gbvision.utils.readable import Readable


class WrapperWindow(Readable, Window, abc.ABC):
    """
    A window class that uses an object (wrap_object) and reads frames from it in to display it's feed
    The window is also a readable, calling "read" will show a frame and return it

    :param wrap_object: An object to read frames from, can be of any type
    """

    def __init__(self, window_name: str, wrap_object: Any, drawing_pipeline=EMPTY_PIPELINE):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.wrap_object = wrap_object
        self.__width = 0
        self.__height = 0

    def read(self) -> Tuple[bool, Frame]:
        """
        Shows one frame and returns it

        :return: The frame if the window was not closed, None otherwise
        """
        ok, frame = self._get_frame()
        if ok and self.show_frame(frame):
            self.__width = frame.shape[1]
            self.__height = frame.shape[0]
            return True, frame
        return False, None

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def show(self) -> None:
        """
        Reads from the wrap object and shows the frame until the window is closed
        """
        while True:
            if not self.read()[0]:
                return

    @abc.abstractmethod
    def _get_frame(self) -> Tuple[bool, Frame]:
        """
        Unsafely reads a frame from the wrapped object and returns the read frame
        
        :return: A tuple of two values, the first is a boolean indicating if the method has succeded, the second is
                 the read frame (or None on failure)
        """

    def show_async(self) -> None:
        """
        Opens the steam video window on another thread
        """
        # Close existing window to allow it to re-open on the new thread
        if self.is_opened():
            self.release()
        Thread(target=self.show).start()
