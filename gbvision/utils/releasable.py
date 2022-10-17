import abc


class Releasable(abc.ABC):
    """
    An interface representing an object holding some resources, which can be released
    """

    @abc.abstractmethod
    def release(self) -> None:
        """
        Closes this releasable and releases it's resource
        """

    @abc.abstractmethod
    def is_opened(self) -> bool:
        """
        Checks if this releasable is open and can be read from

        :return: True if the releasable is opened, False otherwise
        """

    def __enter__(self) -> 'Releasable':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.is_opened():
            self.release()

    def __del__(self) -> None:
        if self.is_opened():
            self.release()
