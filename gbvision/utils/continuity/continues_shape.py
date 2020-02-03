import abc

from gbvision.constants.types import Rect, Number, Frame, Point, Shape
from gbvision.utils.shapes.base_shape import BaseShapeType
from gbvision.utils.tracker import Tracker


class ContinuesShape(abc.ABC):
    """
    An abstract class who's target is to determine in which case two shapes are describing
    the same object, and by that represent a shape in a continues matter.

    in case that no shape matching the object is found then the tracker is deployed by using force_update.

    :param shape: the shape to track with continuity
    :param frame: the frame from which the shape was taken
    :param tracker: optional, a tracker used to track the object if it wasn't found with continuity (default is an empty tracker)
    :param max_area_ratio: the maximum ration between areas of the current shape and another shape \
     so that they can be thought of as the same, default is 2.0
    :param max_distance_ratio: the maximum ratio between the sum of areas of this shape and another and their distance, default is 0.1
    """

    def __init__(self, shape, frame: Frame, tracker: Tracker = None, max_area_ratio=2.0,
                 max_distance_ratio=2.0):  # initialization method of the abstract class
        assert max_area_ratio > 1.0  # sets maximum area ratio as 1
        self._shape = shape  # shape describing the object
        self._count = 0  # the count of how many frames the object cannot be found
        self._tracker = Tracker() if tracker is None else tracker  # Tracker setup in case object is not found
        self._tracker.init(frame, self._to_bounding_rect(shape))
        self.max_area_ratio = max_area_ratio  # setting the maximum bound to which the area difference between the
        # two shapes can be withstanded until it declared as not the same object
        self.max_distance_ratio = max_distance_ratio  # same goes here except it refers to distance between shapes

    @staticmethod
    @abc.abstractmethod
    def _base_shape() -> BaseShapeType:
        """
        returns the base shape matching this continues shape

        :return: the base shape (a class that inherits from BaseShape)
        """

    def _shape_collision(self, shape: Shape) -> bool:
        return self._base_shape().shape_collision(self._shape, shape)

    @classmethod
    def _shape_area(cls, shape: Shape) -> Number:
        return cls._base_shape().shape_area(shape)

    @classmethod
    def _shape_center(cls, shape: Shape) -> Point:
        return cls._base_shape().shape_center(shape)

    @staticmethod
    @abc.abstractmethod
    def _from_bounding_rect(bounding_rect: Rect) -> Shape:
        """
        a function which finds a shape according to its bounding rectangle
        :param: the rectangle bounding the shape
        :return: a shape that is bound by the bounding rect
        """

    @staticmethod
    @abc.abstractmethod
    def _to_bounding_rect(shape: Shape) -> Rect:
        """
        finds a rectangle bounding a shape
        :param shape: the shape's bounding rectangle you wish to find
        :return: a rectangle which bounds the shape given
        """

    def _shape_square_distance(self, other_shape: Shape) -> Number:
        """
        a method which finds the distance between the centers of the object shape and another one
        :param other_shape: the other shape you want to check the distance to
        :return: the distance between the shape squared in order to save computing of square root (pythagorean theorem)
        """
        self_center, other_center = self._shape_center(self._shape), self._shape_center(other_shape)
        return (other_center[0] - self_center[0]) ** 2 + \
               (other_center[1] - self_center[1]) ** 2

    def _is_legal(self, shape: Shape) -> bool:
        """
        checks a variety of different relations between to shapes to determine whether it describes the same object or not
        :param shape: the other shape comparing to the current one
        :return: true or false, same or different
        """
        if self._shape_collision(shape):
            if 1.0 / self.max_area_ratio <= self._shape_area(self._shape) / self._shape_area(
                    shape) <= self.max_area_ratio:
                if self._shape_square_distance(shape) <= (
                        self._shape_area(self._shape) + self._shape_area(shape)) * self.max_distance_ratio:
                    return True
        return False

    def get(self) -> Shape:
        """
        retrieve the shape that this continues shape tracks

        :return: this continues shape's inner shape
        """
        return self._shape

    def update(self, shape: Shape, frame: Frame) -> bool:
        """
        an annual check updating the location and data of the object
        :param shape: the shape suspect as the same object
        :param frame: the frame on which the suspect shape is
        :return: true or false, same shape, not the same shape
        """
        if self._is_legal(shape):
            self._shape = shape
            self._count = 0
            self._tracker.init(frame, self._to_bounding_rect(shape))
            return True
        return False

    def update_forced(self, frame: Frame):
        """
        an update which happens when you lost the shape with continuity
        :param frame: the frame on which opencv2 tracking is happening
        """
        self._shape = self._from_bounding_rect(self._tracker.update(frame))
        self._count += 1

    def is_lost(self, max_count: int) -> bool:
        """
        check if it has been too long (more that max_count frames) since you last saw the object

        :param max_count:the maximum amount of frames tolerable before the shape is declared lost, None is infinity
        :return: lost or not
        """
        return max_count is not None and self._count > max_count
