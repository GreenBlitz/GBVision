from .recording_window import RecordingWindow
from .opencv_window import OpenCVWindow
from gbvision.models.system import EMPTY_PIPELINE
from os.path import splitext
import cv2
from gbvision.constants.video import VIDEO_FILE_TYPE


class RecordingOpenCVWindow(OpenCVWindow, RecordingWindow):
    """
    :param file_name: the name of the output file
    :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
    :param exit_button: an array of keys (a string), when one of the keys are pressed the window will be closed
    :param window_name: the title of the window
    :param fps: the fps of the video file
    :param recording_pipeline: optional, a drawing pipeline to run on the frames being recorded
    """

    def __init__(self, window_name: str, file_name: str, fps=20.0, exit_button='qQ',
                 drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE, width=0, height=0,
                 flags=cv2.WINDOW_FREERATIO):
        """
        initializes the stream window
        
        """
        OpenCVWindow.__init__(self, window_name, exit_button=exit_button, flags=flags)
        RecordingWindow.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline,
                                 recording_pipeline=recording_pipeline)
        self.file_name = file_name

        _, file_ext = splitext(file_name)

        self.fourcc = cv2.VideoWriter_fourcc(*VIDEO_FILE_TYPE[file_ext.upper()])

        self.fps = fps

        self.video_writer = None
        self.width = width
        self.height = height

    def _record(self, frame):
        if frame is None or len(frame.shape) == 0:
            return
        if self.video_writer is None:
            width = self.width if self.width != 0 else frame.shape[1]
            height = self.height if self.height != 0 else frame.shape[0]
            self.video_writer = cv2.VideoWriter(self.file_name, self.fourcc, self.fps, (width, height))
        self.video_writer.write(frame)
