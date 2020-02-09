import abc

from gbvision.constants.types import Frame


class Recorder(abc.ABC):
    def __init__(self, file_name):
        self.file_name = file_name

    @abc.abstractmethod
    def record(self, frame: Frame):
        """
        records the frame

        :param frame: the frame to record
        """

    @abc.abstractmethod
    def close(self):
        """
        ends the writing to the file

        """