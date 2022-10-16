from .recording_window import RecordingWindow
from .opencv_window import OpenCVWindow
from gbvision.models.system import EMPTY_PIPELINE
import cv2
from gbvision.utils.recorders.opencv_recorder import OpenCVRecorder


class RecordingOpenCVWindow(OpenCVWindow, RecordingWindow):
    """
    A basic recording window that uses an OpenCVRecorder to record videos

    :param file_name: The name of the output file
    :param drawing_pipeline: Optional. A pipeline of drawing functions that will run on the frame before displaying
        it
    :param exit_button: An array of keys (a string), when one of the keys are pressed the window will be closed
    :param window_name: The title of the window
    :param fps: The fps of the video file
    :param recording_pipeline: Optional, A drawing pipeline to run on the frames being recorded
    """

    def __init__(self, window_name: str, file_name: str, fps=20.0, exit_button='qQ',
                 drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE, width=None, height=None,
                 flags=cv2.WINDOW_FREERATIO):
        recorder = OpenCVRecorder(file_name, fps, width, height)
        OpenCVWindow.__init__(self, window_name, exit_button=exit_button, flags=flags)
        RecordingWindow.__init__(self, window_name=window_name, recorder=recorder, drawing_pipeline=drawing_pipeline,
                                 recording_pipeline=recording_pipeline)

    def _release(self):
        OpenCVWindow._release(self)
        RecordingWindow._release(self)
