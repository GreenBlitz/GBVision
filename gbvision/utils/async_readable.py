import abc
import time
from threading import Thread
from typing import Tuple

from gbvision.constants.types import Frame
from gbvision.utils.readable import Readable


class AsyncReadable(Readable, abc.ABC):
    """
    an async readable class that constantly reads on another thread
    """

    def __init__(self):
        self.__ok, self.__frame = False, None
        self.__thread = Thread(target=self.__async_read_wrapper)
        self.__thread.start()

    def read(self):
        return self.__ok, self.__frame

    def has_started_reading(self) -> bool:
        """
        checks if the async thread has started reading

        :return: True if the async thread started, False otherwise
        """
        return self.__ok

    def wait_start_reading(self, wait_time=0.01):
        """
        waits until the async thread starts reading

        :param wait_time: amounts of seconds to wait in every check interval, default is 0.01
        :return:
        """
        while not self.has_started_reading():
            time.sleep(wait_time)

    @abc.abstractmethod
    def _read(self) -> Tuple[bool, Frame]:
        """
        reads from the camera synchronously (similar to Readable.read), unsafe, not to use by the programmer
        this method will usually simply call super(self, ReadableClass).read()

        :return: tuple of bool (indicates if read was successful) and the frame (if successful, else None)
        """

    def __async_read_wrapper(self):
        while True:
            self.__ok, self.__frame = self._read()
