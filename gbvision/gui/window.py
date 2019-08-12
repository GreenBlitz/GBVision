from gbvision.exceptions import AbstractMethodCallingException
from gbvision.constants.system import EMPTY_PIPELINE


class Window:
    """
    an abstract window class
    """
    def __init__(self, window_name: str, drawing_pipeline=EMPTY_PIPELINE):
        """
        initializes the window
        :param window_name: the title of the new window
        :param drawing_pipeline: optional, a pipeline that draws on each frame before displaying it
        """
        self.window_name = window_name
        self._is_opened = False
        self.drawing_pipeline = drawing_pipeline

    def _show_frame(self, frame) -> bool:
        """
        shows the frame
        :param frame: the frame to show
        :return: False if the window should be closed, True otherwise
        """
        raise AbstractMethodCallingException()

    def is_opened(self) -> bool:
        """

        :return: True is the window is opened, False otherwise
        """
        return self._is_opened

    def show_frame(self, frame) -> bool:
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

    def _open(self):
        raise AbstractMethodCallingException()

    def _close(self):
        raise AbstractMethodCallingException()

    def open(self):
        """
        opens the window
        """
        self._open()
        self._is_opened = True

    def close(self):
        """
        closes the window
        :return:
        """
        self._close()
        self._is_opened = False