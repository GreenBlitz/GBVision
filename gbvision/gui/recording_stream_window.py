from .recording_wrapper_opencv_window import RecordingWrapperOpenCVWindow
from .stream_window import StreamWindow


class RecordingStreamWindow(RecordingWrapperOpenCVWindow, StreamWindow):
    """
    a basic window that displays the stream from a stream receiver
    and records the stream to a video file
    """
