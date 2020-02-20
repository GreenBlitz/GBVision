import abc
from typing import List, Iterable

from gbvision.utils.cameras.camera import Camera

from gbvision.constants.types import Frame, Location, Number, Point, Shape
from gbvision.utils.game_object import GameObject
from gbvision.utils.shapes.base_shape import BaseShapeType


class ObjectFinder(abc.ABC):
    """
    this is an abstract class that represents an object finder
    an object finder is a type that outputs an object's 3d real location based on an of it image it's
    GameObject real-life parameters

    :param game_object: the game object descriptor for the real-life parameters of the finder's target
    :param area_scalar: a scalar to multiply the root of the area of the shape in the image by, default is 1
    """

    def __init__(self, game_object: GameObject, area_scalar=1.0):
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

    @staticmethod
    @abc.abstractmethod
    def _base_shape() -> BaseShapeType:
        """
        returns the base shape matching this finder

        :return: the base shape (a class that inherits from BaseShape)
        """

    @abc.abstractmethod
    def find_shapes_unsorted(self, frame: Frame) -> List[Shape]:
        """
        finds all the objects and returns them in frame after full pipeline (not sorted)

        :param: The current frame the finder searches in
        :return: A list of objects: see gbvision/constants/types
        """

    def find_shapes(self, frame: Frame) -> List[Shape]:
        """
        finds all the objects and returns them in frame after full pipeline (sorted)

        :param: The current frame the finder searches in
        :return: A list of objects: see gbvision/constants/types
        """
        return self._base_shape().sort_shapes(self.find_shapes_unsorted(frame))

    @classmethod
    def _shape_root_area(cls, shape: Shape) -> Number:
        return cls._base_shape().shape_root_area(shape)

    @classmethod
    def _shape_center(cls, shape: Shape) -> Point:
        return cls._base_shape().shape_center(shape)

    def filter_inner_shapes(self, shapes: List[Shape]) -> List[Shape]:
        """
        filters out all inner shapes in the given sorted list of shapes

        :param shapes: a sorted list of shapes
        :return: the list of shapes, without any shape intersecting with a larger shape
        """
        return self._base_shape().filter_inner_shapes(shapes)

    def locations_from_shapes(self, shapes: Iterable[Shape], camera: Camera) -> List[Location]:
        """
        finds the locations of the shapes based on the shape descriptor and camera constants

        :param shapes: a list of the shapes
        :param camera: the camera used to capture the frame that the shapes were found in
        :return: a list of the locations of all the shapes
        """
        return list(
            map(lambda shape: self.game_object.location_by_params(camera,
                                                                  self._shape_root_area(shape) * self.area_scalar,
                                                                  self._shape_center(shape)), shapes))
