from .wrapper_opencv_window import WrapperOpenCVWindow
from gbvision.utils.readable import Readable


class ReadableWindow(WrapperOpenCVWindow):
    """
    a basic window that displays the stream from any readable

    :type self.wrap_object: gbvision.Readable
    """

    def __init__(self, window_name: str, wrap_object: Readable, *args, **kwargs):
        WrapperOpenCVWindow.__init__(self, window_name, wrap_object, *args, **kwargs)

    def _get_frame(self):
        _, frame = self.wrap_object.read()
        return frame
