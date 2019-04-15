from .camera import Camera, AbstractMethodCallingException
from net import StreamBroadcaster


class StreamCamera(Camera):
    def is_streaming(self) -> bool:
        raise AbstractMethodCallingException()

    def toggle_stream(self, should_stream: bool):
        raise AbstractMethodCallingException()

    @staticmethod
    def create_type(camera_class):
        class _StreamCamera(camera_class, StreamCamera):
            def __init__(self, broadcaster: StreamBroadcaster, *args, **kwargs):
                camera_class.__init__(self, *args, **kwargs)
                self._is_streaming = False
                self.stream_broadcaster = broadcaster

            def is_streaming(self):
                return self._is_streaming

            def toggle_stream(self, should_stream: bool):
                self._is_streaming = should_stream

            def read(self, frame=None):
                ok, frame = camera_class.read(self)
                if self._is_streaming:
                    self.stream_broadcaster.send_frame(frame)
                return ok, frame

        return _StreamCamera
