from .recording_opencv_window import RecordingOpenCVWindow
from .feed_window import FeedWindow


class RecordingFeedWindow(RecordingOpenCVWindow, FeedWindow):
    """
    A basic window that displays the stream from a stream receiver
    """
