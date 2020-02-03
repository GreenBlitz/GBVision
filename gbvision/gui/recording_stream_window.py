from .recording_readable_window import RecordingReadableWindow
from .stream_window import StreamWindow


class RecordingStreamWindow(RecordingReadableWindow, StreamWindow):
    """
    a basic window that displays the stream from a stream receiver
    and records the stream to a video file
    """
