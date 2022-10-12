import abc
from typing import List, Iterable, Union

from gbvision.models.contours import find_contours
from gbvision.models.system import EMPTY_PIPELINE
from gbvision.utils.thresholds.threshold import Threshold
from gbvision.utils.cameras.camera import Camera

from gbvision.constants.types import Frame, Location, Shape, FilterFunction
from gbvision.utils.game_object import GameObject
from gbvision.utils.shapes.base_shape import BaseShapeType


class ObjectFinder(abc.ABC):
    """
    This is an abstract class that represents an object finder
    An object finder is a type that outputs an object's 3d real location based on an of it image it's
    GameObject real-life parameters

    :param game_object: The game object descriptor for the real-life parameters of the finder's target
    :param area_scalar: A scalar to multiply the root of the area of the shape in the image by, default is 1
    """

    def __init__(
            self,
            game_object: GameObject,
            threshold_func: Union[FilterFunction, Threshold],
            area_scalar=1.0,
            contours_hook: FilterFunction = EMPTY_PIPELINE,
            shapes_hook: FilterFunction = EMPTY_PIPELINE,
    ):
        self.game_object = game_object
        self.area_scalar = area_scalar
        self._find_shapes_pipeline = EMPTY_PIPELINE + \
                                     threshold_func + \
                                     find_contours + \
                                     contours_hook + \
                                     self._base_shape().from_contours + \
                                     shapes_hook

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

    def find_shapes_unsorted(self, frame: Frame) -> List[Shape]:
        """
        finds all the objects and returns them in frame after full pipeline (not sorted)

        :param: The current frame the finder searches in
        :return: A list of objects: see gbvision/constants/types
        """
        return self._find_shapes_pipeline(frame)

    def find_shapes(self, frame: Frame) -> List[Shape]:
        """
        Finds all the objects and returns them in frame after full pipeline (sorted)

        :param: The current frame the finder searches in
        :return: A list of objects: see gbvision/constants/types
        """
        return self._base_shape().sort(self.find_shapes_unsorted(frame))

    def locations_from_shapes(self, shapes: Iterable[Shape], camera: Camera) -> List[Location]:
        """
        Finds the locations of the shapes based on the shape descriptor and camera constants

        :param shapes: a list of the shapes
        :param camera: the camera used to capture the frame that the shapes were found in
        :return: a list of the locations of all the shapes
        """
        return list(
            map(lambda shape: self.game_object.location(camera,
                                                        self._base_shape().root_area(shape) * self.area_scalar,
                                                        self._base_shape().center(shape)), shapes))
