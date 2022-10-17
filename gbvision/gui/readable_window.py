from typing import Tuple

from .wrapper_opencv_window import WrapperOpenCVWindow
from gbvision.utils.readable import Readable
from gbvision.constants.types import Frame


class ReadableWindow(WrapperOpenCVWindow):
    """
    A basic window that displays the stream from any readable

    :param wrap_object: A readable to read the frames from
    """

    def __init__(self, window_name: str, wrap_object: Readable, *args, **kwargs):
        WrapperOpenCVWindow.__init__(self, window_name, wrap_object, *args, **kwargs)

    def _get_frame(self) -> Tuple[bool, Frame]:
        return self.wrap_object.read()
