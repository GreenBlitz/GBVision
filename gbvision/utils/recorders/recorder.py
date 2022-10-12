import abc

from gbvision.constants.types import Frame


class Recorder(abc.ABC):
    """
    An abstract recorder class
    records a given feed of frames into a file

    :param file_name: the file name
    """
    def __init__(self, file_name):
        self.file_name = file_name

    @abc.abstractmethod
    def record(self, frame: Frame) -> Frame:
        """
        records the frame

        :param frame: the frame to record
        """

    @abc.abstractmethod
    def close(self) -> None:
        """
        Ends the writing to the file
        """

    @abc.abstractmethod
    def is_opened(self) -> bool:
        """
        Checks if this video file is opened

        :return: True if this is opened, False otherwise
        """