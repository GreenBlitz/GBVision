import abc
from typing import Tuple
from .releasable import Releasable

from gbvision.constants.types import Frame


class Readable(Releasable, abc.ABC):
    """
    An interface representing an object you can read frames from, such as cameras and streams
    """

    @abc.abstractmethod
    def read(self) -> Tuple[bool, Frame]:
        """
        Reads from the readable and returns the result

        :return: False, None if the operation was unsuccessful, else True, frame_result
        """

    @abc.abstractmethod
    def get_width(self) -> int:
        """
        :return: The width of the frames read by this readable
        """

    @abc.abstractmethod
    def get_height(self) -> int:
        """
        :return: The height of the frames read by this readable
        """
