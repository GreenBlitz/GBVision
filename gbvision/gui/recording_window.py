from .window import Window
from gbvision.exceptions.abstract_method_calling_exception import AbstractMethodCallingException
from gbvision.constants.system import EMPTY_PIPELINE

class RecordingWindow(Window):

    def __init__(self, window_name: str, drawing_pipeline=EMPTY_PIPELINE, recording_pipeline=EMPTY_PIPELINE):
        Window.__init__(self, window_name=window_name, drawing_pipeline=drawing_pipeline)
        self.recording_pipeline = recording_pipeline

    def _record(self, frame):
        raise AbstractMethodCallingException()

    def show_frame(self, frame):
        self._record(self.recording_pipeline(frame))
        return Window.show_frame(self, frame)