import abc
from typing import Tuple

from gbvision.constants.types import Frame


class Readable(abc.ABC):
    """
    an interface representing an object you can read frames from, such as cameras and streams
    """

    @abc.abstractmethod
    def read(self) -> Tuple[bool, Frame]:
        """
        reads from the readable and returns the result

        :return: False, None if the operation was unsuccessful, else True, frame_result
        """
