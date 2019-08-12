from .window import Window
from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.exceptions.abstract_method_calling_exception import AbstractMethodCallingException
from threading import Thread

class WrapperWindow(Window):
    def __init__(self, window_name: str, wrap_object, drawing_pipeline=EMPTY_PIPELINE):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.wrap_object = wrap_object

    def show_and_get_frame(self):
        """
        shows one frame and returns it
        :return: the frame if the window was not closed, None otherwise
        """
        frame = self._get_frame()
        if self.show_frame(frame):
            return frame
        return None

    def show(self):
        """
        reads from the wrap object and shows the frame until the window is closed
        :return:
        """
        while True:
            if self.show_and_get_frame() is None:
                return

    def _get_frame(self):
        raise AbstractMethodCallingException()

    def show_async(self):
        """
        opens the steam video window on another thread
        """
        Thread(target=self.show).start()