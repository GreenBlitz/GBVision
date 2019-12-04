import abc

from gbvision.constants.types import Rect, Number, Frame, Point
from gbvision.utils.tracker import Tracker


class ContinuesShape(abc.ABC):
    '''
    And abstract class which's target is to determine and in which case to act whether two shapes are describing
    the same object, if so it's shape instance is replaced to the current description.

    in case that no shape matching the object is found then the opencv2's Tracker is deployed. if it loses it to
    it sends an appropriate message.
    '''

    def __init__(self, shape, frame: Frame, tracker: Tracker = None, max_area_ratio=2.0,
                 max_distance_ratio=0.1):  # initiat   ion method of the abstract class
        assert max_area_ratio > 1.0  # sets maximum area ratio as 1
        self._shape = shape  # shape describing the object
        self._count = 0  # the count of how many frames the object cannot be found
        self._tracker = Tracker() if tracker is None else tracker  # Tracker setup in case object is not found
        self._tracker.init(frame, self._to_bounding_rect(shape))
        self.max_area_ratio = max_area_ratio  # setting the maximum bound to which the area difference between the two shapes can be withstanded until it declared as not the same object
        self.max_distance_ratio = max_distance_ratio  # same goes here except it refers to distance between shapes

    @abc.abstractmethod
    def _shape_collision(self, shape) -> bool:
        '''
        a function which checks whether a shape is colliding with the current object's shape or not.
        :param: shape: the shape which is tested
        :return: True or False, collides or not.
        '''

    @staticmethod
    @abc.abstractmethod
    def _shape_area(shape) -> Number:
        '''
        a method which calculates a shape's on-screen area
        :param shape: the shape's area you wish to accept
        :return: a number which expresses the shape's area on-screen in M^2
        '''

    @staticmethod
    @abc.abstractmethod
    def _shape_center(shape) -> Point:
        """
        determines a shape's center
        :param shape: the shape's center you wish to find
        :return: the location on-screen of the center point
        """

    @staticmethod
    @abc.abstractmethod
    def _from_bounding_rect(bounding_rect: Rect):
        '''
        a function which finds a shape according to its bounding rectangle
        :param: the rectangle bounding the shape
        :return: a shape that is bound by the bounding rect
        '''

    @staticmethod
    @abc.abstractmethod
    def _to_bounding_rect(shape) -> Rect:
        '''
        finds a rectangle bounding a shape
        :param shape: the shape's bounding rectangle you wish to find
        :return: a rectangle which bounds the shape given
        '''

    def _shape_square_distance(self, other_shape) -> Number:
        '''
        a method which finds the distance between the centers of the object shape and another one
        :param other_shape: the other shape you want to check the distance to
        :return: the distance between the shape squared in order to save computing of square root (pythagorean theorem)
        '''
        return (self._shape_center(other_shape)[0] - self._shape_center(self._shape)[0]) ** 2 + \
               (self._shape_center(other_shape)[1] - self._shape_center(self._shape)[1]) ** 2

    def _is_legal(self, shape) -> bool:
        '''
        checks a variety of different relations between to shapes to determine whether it describes the same object or not
        :param shape: the other shape comparing to the current one
        :return: true or false, same or different
        '''
        if self._shape_collision(shape):
            if 1.0 / self.max_area_ratio <= self._shape_area(self._shape) / self._shape_area(
                    shape) <= self.max_area_ratio:
                if self._shape_square_distance(shape) <= (
                        self._shape_area(self._shape) + self._shape_area(shape)) * self.max_distance_ratio:
                    return True
        return False

    def get(self):#returns the object's describing shape
        return self._shape

    def update(self, shape, frame: Frame) -> bool:
        '''
        an annual check updating the location and data of the object
        :param shape: the shape suspect as the same object
        :param frame: the frame on which the suspect shape is
        :return: true or false, same shape, not the same shape
        '''
        if self._is_legal(shape):
            self._shape = shape
            self._count = 0
            self._tracker.init(frame, self._to_bounding_rect(shape))
            return True
        return False

    def update_forced(self, frame: Frame):
        '''
        an update which happens when you lost the shape with continuity
        :param frame: the frame on which opencv2 tracking is happening
        '''
        self._shape = self._from_bounding_rect(self._tracker.update(frame))
        self._count += 1

    def is_lost(self, max_count: int) -> bool:
        '''

        :param max_count:the maximum amount of frames tolerable before the shape is declared lost
        :return: lost or not
        '''
        return max_count is not None and self._count > max_count
