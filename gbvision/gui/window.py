from threading import Thread

from gbvision.exceptions import AbstractMethodCallingException
from gbvision.utils.pipeline import PipeLine


class Window:
    """
    an abstract window class
    """
    def __init__(self, window_name: str, exit_button='qQ', drawing_pipeline=PipeLine()):
        """
        initializes the window
        :param window_name: the title of the new window
        :param exit_button: the button that closes the window
        :param drawing_pipeline: optional, a pipeline that draws on each frame before displaying it
        """
        self.window_name = window_name
        self.exit_button = exit_button
        self.drawing_pipeline = drawing_pipeline

    def show(self):
        raise AbstractMethodCallingException()

    def show_async(self):
        Thread(target=self.show).start()
