from .recording_wrapper_opencv_window import RecordingWrapperOpenCVWindow
from .camera_window import CameraWindow


class RecordingCameraWindow(RecordingWrapperOpenCVWindow, CameraWindow):
    """
    a basic window that displays the stream from a stream receiver
    """

