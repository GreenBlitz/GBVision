from os.path import splitext
from threading import Thread

import cv2

from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.constants.video import VIDEO_FILE_TYPE
from gbvision.net.stream_receiver import StreamReceiver
from .window import Window


class RecordingStreamWindow(Window):
    """
    a basic window that displays the stream from a stream receiver
    """

    def __init__(self, stream_receiver: StreamReceiver, file_name: str, window_name='stream', fps=20.0,
                 exit_button='qQ', drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE):
        """
        initializes the stream window
        :param stream_receiver: a stream receiver from which the stream receives it's frames
        :param file_name: the name of the output file
        :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
        :param exit_button: an array of keys (a string), when one of the keys are pressed the window will be closed
        :param window_name: the title of the window
        :param fps: the fps of the video file
        :param recording_pipeline: optional, a drawing pipeline to run on each frame of the recorded video
        """
        Window.__init__(self, window_name, exit_button, drawing_pipeline)
        self.stream_receiver = stream_receiver

        self.file_name = file_name

        _, file_ext = splitext(file_name)

        self.fourcc = cv2.VideoWriter_fourcc(*VIDEO_FILE_TYPE[file_ext.upper()])

        self.fps = fps

    def show(self, flags=cv2.WINDOW_FREERATIO):
        """
        display the stream video window
        :param flags: some opencv window flags
        """
        cv2.namedWindow(self.window_name, flags)
        video_writer = None
        while True:
            frame = self.stream_receiver.get_frame()
            if frame is not None:
                if video_writer is None:
                    video_writer = cv2.VideoWriter(self.file_name, self.fourcc, self.fps, frame.shape[:2][::-1])
                video_writer.write(frame)
                cv2.imshow(self.window_name, self.drawing_pipeline(frame))
            k = chr(cv2.waitKey(1) & 0xFF)
            if k in self.exit_button:
                cv2.destroyWindow(self.window_name)
                return

    def show_async(self, flags=cv2.WINDOW_FREERATIO):
        """
        opens the steam video window on another thread
        :param flags: some opencv window flags
        """
        Thread(target=self.show, args=(flags,)).start()
