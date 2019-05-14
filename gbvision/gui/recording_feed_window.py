from os.path import splitext
from threading import Thread

import cv2

from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.constants.video import VIDEO_FILE_TYPE
from .feed_window import FeedWindow


class RecordingFeedWindow(FeedWindow):
    """
    a basic window that displays the stream from a stream receiver
    """

    def __init__(self, file_name: str, window_name: str, fps=20.0, exit_button='qQ',
                 drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE):
        """
        initializes the feed window
        :param file_name: the name of the output file
        :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
        :param exit_button: an array of keys (a string), when one of the keys are pressed the window will be closed
        :param window_name: the title of the window
        :param fps: the fps of the video file
        :param recording_pipeline: optional, a drawing pipeline to run on the frames being recorded
        """
        FeedWindow.__init__(self, window_name=window_name, exit_button=exit_button, drawing_pipeline=drawing_pipeline)
        self.recording_pipeline = recording_pipeline
        self.file_name = file_name

        _, file_ext = splitext(file_name)

        self.fourcc = cv2.VideoWriter_fourcc(*VIDEO_FILE_TYPE[file_ext.upper()])

        self.fps = fps
        self.video_writer = None

    def show_frame(self, frame):
        """
        display the stream video window
        :param frame: the frame to show
        """
        if self.video_writer is None and frame is not None:
            self.video_writer = cv2.VideoWriter(self.file_name, self.fourcc, self.fps, frame.shape[:2][::-1])
        self.video_writer.write(self.recording_pipeline(frame))
        return FeedWindow.show_frame(self, frame)
