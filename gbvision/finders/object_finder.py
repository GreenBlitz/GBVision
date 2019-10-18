import abc

from gbvision.constants.types import Frame
from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.utils.game_object import GameObject, Camera


class ObjectFinder(abc.ABC):
    """
    this is an abstract class that represents an object finder
    an object finder is a type that outputs an object's 3d real location based on an of it image it's
    GameObject real-life parameters
    """

    def __init__(self, threshold_func, game_object: GameObject):
        """
        initializes the finder
        :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
        the finder is searching, the object needs to be white and the rest if the image black (doesn't
        have to be perfect)
        :param game_object: the game object descriptor for the real-life parameters of the finder's target
        """
        self.threshold = EMPTY_PIPELINE + threshold_func
        self.game_object = game_object

    @abc.abstractmethod
    def __call__(self, frame: Frame, camera: Camera):
        """
        finds all instances of the object in the frame
        :param frame: the frame in which to find
        :param camera: the camera used to read the frame
        :return: all object of this type in the physical space
        """
        pass
