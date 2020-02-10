import abc

from gbvision.models.system import EMPTY_PIPELINE
from gbvision.constants.types import Frame


class Window(abc.ABC):
    """
    an abstract window class

    :param window_name: the title of the new window
    :param drawing_pipeline: optional, a pipeline that draws on each frame before displaying it
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
        shows the frame
        :param frame: the frame to show
        :return: False if the window should be closed, True otherwise
        """

    def is_opened(self) -> bool:
        """

        :return: True is the window is opened, False otherwise
        """
        return self._is_opened

    def show_frame(self, frame: Frame) -> bool:
        """
        shows the frame on the window
        :param frame: the frame to show
        :return: false if the window was closed, true otherwise
        """
        if not self.is_opened():
            self.open()
        if self._show_frame(self.drawing_pipeline(frame)):
            return True
        self.close()
        return False

    @abc.abstractmethod
    def _open(self):
        """
        unsafely opens the window
        not to be used by the programmer, only by the function open
        """

    @abc.abstractmethod
    def _close(self):
        """
        unsafely closes the window
        not to be used by the programmer, only by the function close
        """

    def open(self):
        """
        opens the window
        """
        self._open()
        self._is_opened = True

    def close(self):
        """
        closes the window
        """
        self._close()
        self._is_opened = False

    def __del__(self):
        self.close()
