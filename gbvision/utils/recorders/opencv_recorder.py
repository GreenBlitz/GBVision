from os.path import splitext
from typing import Optional

import cv2
from gbvision.constants.video import VIDEO_FILE_TYPE

from .recorder import Recorder


class OpenCVRecorder(Recorder):
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
            width = self.width if self.width is not None else frame.shape[1]
            height = self.height if self.height is not None else frame.shape[0]
            self.video_writer = cv2.VideoWriter()
            self.video_writer.open(self.file_name, self.fourcc, self.fps, (width, height))
        self.video_writer.write(frame)

    def close(self):
        self.video_writer.release()
