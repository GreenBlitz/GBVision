import abc

from gbvision.utils.releasable import Releasable
from gbvision.models.system import EMPTY_PIPELINE
from gbvision.constants.types import Frame


class Window(Releasable, abc.ABC):
    """
    An abstract window class

    :param window_name: The title of the new window
    :param drawing_pipeline: Optional. A pipeline that draws on each frame before displaying it
    """

    def __init__(self, window_name: str, drawing_pipeline=EMPTY_PIPELINE):
        """
        initializes the window
        """
        self.window_name = window_name
        self._is_opened = False
        self.drawing_pipeline = drawing_pipeline

    @abc.abstractmethod
    def _show_frame(self, frame: Frame) -> bool:
        """
        Shows the frame
        :param frame: the frame to show
        :return: False if the window should be closed, True otherwise
        """

    def is_opened(self) -> bool:
        """
        Checks if the window is opened

        :return: True is the window is opened, False otherwise
        """
        return self._is_opened

    def show_frame(self, frame: Frame) -> bool:
        """
        Shows the frame on the window

        :param frame: the frame to show
        :return: false if the window was closed, true otherwise
        """
        if not self.is_opened():
            self.open()
        if self._show_frame(self.drawing_pipeline(frame)):
            return True
        self.release()
        return False

    def show_and_return_frame(self, frame: Frame) -> Frame:
        """
        Shows and returns the given frame

        :param frame: The frame to show
        :return: The given frame, or None if the window has closed
        """
        return frame if self.show_frame(frame) else None

    @abc.abstractmethod
    def _open(self) -> None:
        """
        Unsafely opens the window
        Not to be used by the programmer, only by the function open
        """

    @abc.abstractmethod
    def _release(self) -> None:
        """
        Unsafely closes the window
        Not to be used by the programmer, only by the function close
        """

    def open(self) -> None:
        """
        Opens the window
        """
        if not self.is_opened():
            self._open()
            self._is_opened = True

    def release(self) -> None:
        """
        Closes the window
        """
        if self.is_opened():
            self._release()
            self._is_opened = False
