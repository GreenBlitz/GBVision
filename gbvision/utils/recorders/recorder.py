import abc

from gbvision.utils.releasable import Releasable
from gbvision.constants.types import Frame


class Recorder(Releasable, abc.ABC):
    """
    An abstract recorder class
    Records a given feed of frames into a file

    :param file_name: the file name
    """
    def __init__(self, file_name):
        self.file_name = file_name

    @abc.abstractmethod
    def write(self, frame: Frame) -> Frame:
        """
        Writes the given frame to the file

        :param frame: the frame to write
        """
