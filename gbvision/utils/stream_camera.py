from .camera import Camera, AbstractMethodCallingException
from net import StreamBroadcaster


class StreamCamera(Camera):
    """
    an abstract class that represents a streaming camera
    the streaming camera is very similar to a regular camera, but has an option
    which allows it to stream the frames when it reads them
    """
    def is_streaming(self) -> bool:
        """
        checks if the camera is currently streaming
        :return: True if camera is streaming, otherwise Fasle
        """
        raise AbstractMethodCallingException()

    def toggle_stream(self, should_stream: bool):
        """
        turn on or off the stream feature
        :param should_stream: True to activate stream, False to deactivate
        """
        raise AbstractMethodCallingException()

    @staticmethod
    def create_type(camera_class):
        """
        creates a new class that is similar to the given class, but has the stream feature
        the constructor of the new class is the same as the given class, but adds a new parameter at the beginning
        the first parameter to the new constructor is a stream broadcaster
        :param camera_class: the class to wrap
        :return: the wrapped class
        """
        class _StreamCamera(camera_class, StreamCamera):
            def __init__(self, broadcaster: StreamBroadcaster, *args, **kwargs):
                camera_class.__init__(self, *args, **kwargs)
                self._is_streaming = False
                self.stream_broadcaster = broadcaster

            def is_streaming(self):
                return self._is_streaming

            def toggle_stream(self, should_stream: bool):
                self._is_streaming = should_stream

            def read(self, image=None):
                ok, frame = camera_class.read(self, image=image)
                if self._is_streaming:
                    self.stream_broadcaster.send_frame(frame)
                return ok, frame

        return _StreamCamera
