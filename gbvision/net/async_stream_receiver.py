import abc
from threading import Thread

from gbvision.constants.types import Frame
from gbvision.exceptions.stream_closed import StreamClosed
from gbvision.net.stream_receiver import StreamReceiver


class AsyncStreamReceiver(StreamReceiver, abc.ABC):
    """
    an abstract async tcp stream receiver that receives frames on another thread
    None! when inheriting from this class and another StreamReceiver class, make sure you call the other class'
    constructor before this class' constructor, but also make sure you inherit from this class first in order
    """

    def __init__(self, *args, **kwargs):
        StreamReceiver.__init__(self, *args, **kwargs)
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
        reads a frame from the stream synchronously (similar to StreamReceiver.get_frame).
        unsafe not to be used by programmer
        :return: the frame read
        """
        pass

    def read(self):
        return self.__frame
