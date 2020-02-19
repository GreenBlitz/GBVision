import abc

from .window import Window
from gbvision.models.system import EMPTY_PIPELINE
from gbvision.utils.recorders.recorder import Recorder


class RecordingWindow(Window, abc.ABC):
    """
    A basic window that records the stream it receives

    :param recording_pipeline: a drawing pipeline to run on the recorded frame, usually you will want this to be the
        same as the drawing pipeline
    """

    def __init__(self, window_name: str, recorder: Recorder, drawing_pipeline=EMPTY_PIPELINE,
                 recording_pipeline=EMPTY_PIPELINE):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.recording_pipeline = recording_pipeline
        self.recorder = recorder

    def show_frame(self, frame):
        self.recorder.record(self.recording_pipeline(frame))
        return Window.show_frame(self, frame)

    def _close(self):
        self.recorder.close()
