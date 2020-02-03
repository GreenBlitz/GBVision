from .recording_wrapper_opencv_window import RecordingWrapperOpenCVWindow
from .readable_window import ReadableWindow


class RecordingReadableWindow(RecordingWrapperOpenCVWindow, ReadableWindow):
    """
    a basic window that displays the video from a readable
    and records the video to a file
    """
