from .recording_window import RecordingWindow
from .opencv_window import OpenCVWindow
from gbvision.models.system import EMPTY_PIPELINE
from os.path import splitext
import cv2
from gbvision.constants.video import VIDEO_FILE_TYPE
from gbvision.utils.recorders.opencv_recorder import OpenCVRecorder


class RecordingOpenCVWindow(OpenCVWindow, RecordingWindow):
    """
    A basic recording window that uses an OpenCVRecorder to record videos

    :param file_name: the name of the output file
    :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
    :param exit_button: an array of keys (a string), when one of the keys are pressed the window will be closed
    :param window_name: the title of the window
    :param fps: the fps of the video file
    :param recording_pipeline: optional, a drawing pipeline to run on the frames being recorded
    """

    def __init__(self, window_name: str, file_name: str, fps=20.0, exit_button='qQ',
                 drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE, width=None, height=None,
                 flags=cv2.WINDOW_FREERATIO):
        """
        initializes the stream window
        
        """

        recorder = OpenCVRecorder(file_name, fps, width, height)
        OpenCVWindow.__init__(self, window_name, exit_button=exit_button, flags=flags)
        RecordingWindow.__init__(self, window_name=window_name, recorder=recorder, drawing_pipeline=drawing_pipeline,
                                 recording_pipeline=recording_pipeline)

    def _close(self):
        OpenCVWindow._close(self)
        RecordingWindow._close(self)
