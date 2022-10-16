from os.path import splitext

import cv2
from gbvision.constants.video import VIDEO_FILE_TYPE

from .recorder import Recorder


class OpenCVRecorder(cv2.VideoWriter, Recorder):
    """
    A basic implementation of the recorder class using OpenCV

    :param file_name: The path to the output file
    :param fps: The fps of the video
    :param width: Optional. The width of the video (will be set automatically if not given)
    :param height: Optional. The height of the video (will be set automatically if not given)
    """
    def __init__(self, file_name, fps, width=None, height=None):
        Recorder.__init__(self, file_name)
        cv2.VideoWriter.__init__(self)

        _, file_ext = splitext(file_name)

        self.fourcc = cv2.VideoWriter_fourcc(*VIDEO_FILE_TYPE[file_ext.upper()])

        self.fps = fps

        self.width = width
        self.height = height
        self.__initialized = False

    def write(self, frame):
        if frame is None or len(frame.shape) == 0:
            return
        if not self.__initialized:
            self.width = self.width if self.width is not None else frame.shape[1]
            self.height = self.height if self.height is not None else frame.shape[0]
            self.open(self.file_name, self.fourcc, self.fps, (self.width, self.height))
            self.__initialized = True
        cv2.VideoWriter.write(self, frame)
        return frame

    def release(self) -> None:
        cv2.VideoWriter.release(self)

    def is_opened(self) -> bool:
        if not self.__initialized:
            return True
        return self.isOpened()
