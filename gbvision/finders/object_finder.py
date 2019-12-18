import abc
from typing import List, Any

from gbvision.constants.types import Frame, FilterFunction, Location, Number, Point
from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.utils.game_object import GameObject, Camera


class ObjectFinder(abc.ABC):
    """
    this is an abstract class that represents an object finder
    an object finder is a type that outputs an object's 3d real location based on an of it image it's
    GameObject real-life parameters


     :param threshold_func: a pipeline (or any sort of function) that returns a binary threshold of the object
     the finder is searching, the object needs to be white and the rest if the image black (doesn't
     have to be perfect)
     :param game_object: the game object descriptor for the real-life parameters of the finder's target
     :param area_scalar: a scalar to multiply the root of the area of the shape in the image by, default is 1
    """

    def __init__(self, threshold_func: FilterFunction, game_object: GameObject, area_scalar=1.0):
        self.threshold = EMPTY_PIPELINE + threshold_func
        self.game_object = game_object
        self.area_scalar = area_scalar

    def __call__(self, frame: Frame, camera: Camera) -> List[Location]:
        """
        finds all instances of the object in the frame

        :param frame: the frame in which to find
        :param camera: the camera used to read the frame
        :return: all object of this type in the physical space
        """
        return self.locations_from_shapes(self.find_shapes(frame), camera)

    @abc.abstractmethod
    def find_shapes(self, frame: Frame) -> List[Any]:
        """
        finds all the objects and returns them in frame after full pipeline

        :param: The current frame the finder searches in
        :return: A list of objects: see gbvision/constants/types
        """

    @staticmethod
    @abc.abstractmethod
    def _shape_root_area(shape: Any) -> Number:
        """
        calculates the square root of the area of a shape, to be used by the api

        :param shape: the shape
        :return: the area
        """

    @staticmethod
    @abc.abstractmethod
    def _shape_center(shape: Any) -> Point:
        """
        finds the center of the shape, to be used by the api

        :param shape: the shape
        :return: the center of the shape
        """

    def locations_from_shapes(self, shapes: List[Any], camera: Camera) -> List[Location]:
        """
        finds the locations of the shapes based on the shape descriptor and camera constants

        :param shapes: a list of the shapes
        :param camera: the camera used to capture the frame that the shapes were found in
        :return: a list of the locations of all the shapes
        """
        return list(
            map(lambda shape: self.game_object.location_by_params(camera, self._shape_root_area(shape) * self.area_scalar,
                                                                  self._shape_center(shape)), shapes))
