import abc
from typing import List, Iterable, Union, Callable

from gbvision.constants.types import Frame, Location, Shape, FilterFunction, Contour, Number
from gbvision.models.contours import find_contours
from gbvision.models.system import EMPTY_PIPELINE, EMPTY_GAME_OBJECT
from gbvision.utils.cameras.camera import Camera
from gbvision.utils.game_object import GameObject
from gbvision.utils.shapes.base_shape import BaseShapeType
from gbvision.utils.thresholds.threshold import Threshold


class ObjectFinder(abc.ABC):
    """
    This is an abstract class that represents an object finder
    An object finder is a type that outputs an object's 3d real location based on an of it image it's
    GameObject real-life parameters

    :param threshold_func: The threshold function used to find the shapes in the frame
    :param game_object: The game object descriptor for the real-life parameters of the finder's target
    :param contours_hook: Optional. A pipeline to run on the contours after finding them
    :param shapes_hook: Optional. A pipeline to run on the shapes after parsing the contours to them
    """

    def __init__(
            self,
            threshold_func: Union[FilterFunction, Threshold],
            game_object: GameObject = EMPTY_GAME_OBJECT,
            contours_hook: Callable[[List[Contour]], List[Contour]] = EMPTY_PIPELINE,
            shapes_hook: Callable[[List[Shape]], List[Shape]] = EMPTY_PIPELINE,
    ):
        self.game_object = game_object
        self._find_shapes_pipeline = EMPTY_PIPELINE + \
                                     threshold_func + \
                                     find_contours + \
                                     contours_hook + \
                                     self._base_shape().from_contours + \
                                     shapes_hook

    def __call__(self, frame: Frame, camera: Camera) -> List[Location]:
        """
        Finds all instances of the object in the frame

        :param frame: The frame in which to find
        :param camera: The camera used to read the frame
        :return: All object of this type in the physical space
        """
        return self.locations_from_shapes(self.find_shapes(frame), camera)

    @staticmethod
    @abc.abstractmethod
    def _base_shape() -> BaseShapeType:
        """
        Returns the base shape matching this finder

        :return: The base shape (a class that inherits from BaseShape)
        """

    def find_shapes_unsorted(self, frame: Frame) -> List[Shape]:
        """
        Finds all the shapes and returns them in frame after full pipeline (not sorted)

        :param: The current frame the finder searches in
        :return: A list of shapes: see gbvision/constants/types
        """
        return self._find_shapes_pipeline(frame)

    def find_shapes(self, frame: Frame) -> List[Shape]:
        """
        Finds all the shapes and returns them in frame after full pipeline (sorted)

        :param: The current frame the finder searches in
        :return: A list of shapes: see gbvision/constants/types
        """
        return self._base_shape().sort(self.find_shapes_unsorted(frame))

    def find_and_filter_shapes(self, frame: Frame) -> List[Shape]:
        """
        Finds all the shapes and returns them in frame after full pipeline (sorted), removes all inner shapes

        :param: The current frame the finder searches in
        :return: A list of shapes: see gbvision/constants/types
        """
        return self._base_shape().filter_inners(self.find_shapes(frame))

    def locations_from_shapes(self, shapes: Iterable[Shape], camera: Camera) -> List[Location]:
        """
        Finds the locations of the shapes based on the shape descriptor and camera constants

        :param shapes: A list of the shapes
        :param camera: The camera used to capture the frame that the shapes were found in
        :return: A list of the locations of all the shapes
        """
        return list(
            map(lambda shape: self.game_object.location(camera,
                                                        self._base_shape().root_area(shape),
                                                        self._base_shape().center(shape)), shapes))
