import abc
import time
from threading import Thread
from typing import Tuple

from gbvision.constants.types import Frame, Number
from gbvision.utils.readable import Readable


class AsyncReadable(Readable, abc.ABC):
    """
    An async readable class that constantly reads on another thread
    """

    def __init__(self):
        self.__ok, self.__frame = False, None
        self.__is_running = True
        self.__thread = Thread(target=self.__async_read_wrapper)
        self.__thread.start()

    def read(self) -> Tuple[bool, Frame]:
        return self.__ok, self.__frame

    def has_started_reading(self) -> bool:
        """
        Checks if the async thread has started reading

        :return: True if the async thread started, False otherwise
        """
        return self.__ok

    def wait_start_reading(self, wait_time: Number = 0.01) -> None:
        """
        Waits until the async thread starts reading

        :param wait_time: Amounts of seconds to wait in every check interval, default is 0.01
        """
        while not self.has_started_reading():
            time.sleep(wait_time)

    @abc.abstractmethod
    def _read(self) -> Tuple[bool, Frame]:
        """
        Reads from the camera synchronously (similar to Readable.read), unsafe, not to use by the programmer
        this method will usually simply call super(self, ReadableClass).read()

        :return: Tuple of bool (indicates if read was successful) and the frame (if successful, else None)
        """

    def __async_read_wrapper(self) -> None:
        while self.__is_running:
            self.__ok, self.__frame = self._read()

    def release(self) -> None:
        self.__is_running = False
        self.__thread.join()
        self._release()

    @abc.abstractmethod
    def _release(self) -> None:
        """
        Unsafely releases this readable's resources without killing the reading thread
        """