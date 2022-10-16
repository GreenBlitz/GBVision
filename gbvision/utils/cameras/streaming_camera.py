import abc
from typing import Tuple

from gbvision.constants.types import Frame
from gbvision.utils.net.stream_broadcaster import StreamBroadcaster
from .camera import Camera


class StreamingCamera(Camera, abc.ABC):
    """
    An abstract class that represents a streaming camera
    The streaming camera is very similar to a regular camera, but has an option
    which allows it to stream the frames when it reads them
    """

    @abc.abstractmethod
    def is_streaming(self) -> bool:
        """
        Checks if the camera is currently streaming

        :return: True if camera is streaming, otherwise False
        """

    @abc.abstractmethod
    def toggle_stream(self, should_stream: bool):
        """
        Turn on or off the stream feature

        :param should_stream: True to activate stream, False to deactivate
        """

    def read(self):
        ok, frame = self._read()
        self._stream(frame)
        return ok, frame

    @abc.abstractmethod
    def _read(self) -> Tuple[bool, Frame]:
        """
        Unsafely reads from the camera, not to use by the programmer, only by the api
        usually this function is a set to return the value of super(self, CameraClass).read()

        :return: the return value of Camera.read: (ok, frame)
        """

    @abc.abstractmethod
    def _stream(self, frame: Frame):
        """
        Unsafely streams a frame, not to use by the programmer, only by the api

        :param frame: the frame to stream
        """


class SimpleStreamingCamera(StreamingCamera, abc.ABC):
    """
    A simple abstract camera that uses a gbvision.StreamBroadcaster to send streams
    this class is abstract and cannot exist on it's own, you must inherit from it and implement the _read method

    for example:

    Example::
        class USBStreamCamera(SimpleStreamCamera, USBCamera):
            def _read(self) -> Tuple[bool, Frame]:
                return USBCamera.read(self)

            def __init__(self, broadcaster, port, data=UNKNOWN_CAMERA):
                SimpleStreamCamera.__init__(self, broadcaster)
                USBCamera.__init__(port, data)
    """

    def __init__(self, broadcaster: StreamBroadcaster, should_stream=False):
        self.__is_streaming = should_stream
        self.stream_broadcaster = broadcaster

    def is_streaming(self):
        return self.__is_streaming

    def toggle_stream(self, should_stream: bool):
        self.__is_streaming = should_stream

    def _stream(self, frame):
        self.stream_broadcaster.send_frame(frame)
