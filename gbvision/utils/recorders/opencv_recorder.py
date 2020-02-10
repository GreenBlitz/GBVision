from os.path import splitext
from typing import Optional

import cv2
from gbvision.constants.video import VIDEO_FILE_TYPE

from .recorder import Recorder


class OpenCVRecorder(Recorder):
    """
    a basic implementation of the recorder class using OpenCV

    :param file_name: the path to the output file
    :param fps: the fps of the video
    :param width: optional, the width of the video (will be set automatically if not given)
    :param height: optional, the height of the video (will be set automatically if not given)
    """
    def __init__(self, file_name, fps, width=None, height=None):
        Recorder.__init__(self, file_name)

        _, file_ext = splitext(file_name)

        self.fourcc = cv2.VideoWriter_fourcc(*VIDEO_FILE_TYPE[file_ext.upper()])

        self.fps = fps

        self.video_writer: Optional[cv2.VideoWriter] = None
        self.width = width
        self.height = height

    def record(self, frame):
        if frame is None or len(frame.shape) == 0:
            return
        if self.video_writer is None:
            self.width = self.width if self.width is not None else frame.shape[1]
            self.height = self.height if self.height is not None else frame.shape[0]
            self.video_writer = cv2.VideoWriter()
            self.video_writer.open(self.file_name, self.fourcc, self.fps, (self.width, self.height))
        self.video_writer.write(frame)

    def close(self):
        self.video_writer.release()

    def is_opened(self) -> bool:
        if self.video_writer is None:
            return True
        return self.video_writer.isOpened()
