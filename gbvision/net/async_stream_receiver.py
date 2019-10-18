import abc
from threading import Thread

from gbvision.constants.types import Frame
from gbvision.exceptions.stream_closed import StreamClosed
from gbvision.net.stream_receiver import StreamReceiver


class AsyncStreamReceiver(StreamReceiver, abc.ABC):
    def __init__(self, shape=(0, 0), fx: float = 1.0, fy: float = 1.0):
        StreamReceiver.__init__(self, shape, fx, fy)
        self.__frame = None
        self.__thread = Thread(target=self.__receive_thread_function)
        self.__thread.start()

    def __receive_thread_function(self):
        while True:
            try:
                self.__frame = self._get_frame()
            except StreamClosed:
                break

    @abc.abstractmethod
    def _get_frame(self) -> Frame:
        """
        reads a frame from the stream synchronously (similar to StreamReceiver.get_frame). unsafe not to be used by programmer
        :return: the frame read
        """
        pass

    def get_frame(self):
        return self.__frame

    @staticmethod
    def create_type(stream_receiver_class) -> type:
        """
        creates a new class that is similar to the given class, but has the async feature
        the constructor of the new class is the same as the given class
        :param stream_receiver_class: the class to wrap
        :return: the wrapped class as a type that can be instanced
        """

        class _AsyncStreamReceiver(AsyncStreamReceiver, stream_receiver_class):
            def _get_frame(self):
                return stream_receiver_class.get_frame(self)

            def __init__(self, *args, **kwargs):
                stream_receiver_class.__init__(self, *args, **kwargs)
                AsyncStreamReceiver.__init__(self)

        return _AsyncStreamReceiver
