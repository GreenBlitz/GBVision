
from .wrapper_opencv_window import WrapperOpenCVWindow


class StreamWindow(WrapperOpenCVWindow):
    """
    a basic window that displays the stream from a stream receiver
    """

    def _get_frame(self):
        return self.wrap_object.get_frame()
