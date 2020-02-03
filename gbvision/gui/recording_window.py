import abc

from gbvision.constants.types import Frame
from .window import Window
from gbvision.models.system import EMPTY_PIPELINE


class RecordingWindow(Window, abc.ABC):

    def __init__(self, window_name: str, drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.recording_pipeline = recording_pipeline

    @abc.abstractmethod
    def _record(self, frame: Frame):
        """
        unsafely records the given frame
        not to be used by the programmer
        :param frame: the frame to record
        """

    def show_frame(self, frame):
        self._record(self.recording_pipeline(frame))
        return Window.show_frame(self, frame)
