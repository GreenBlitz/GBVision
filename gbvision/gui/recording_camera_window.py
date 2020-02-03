from .recording_readable_window import RecordingReadableWindow
from .camera_window import CameraWindow


class RecordingCameraWindow(RecordingReadableWindow, CameraWindow):
    """
    a basic window that displays the video from a camera
    and records the video to a file
    """
