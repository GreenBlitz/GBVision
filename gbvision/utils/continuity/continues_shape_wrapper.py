from typing import List, Dict, Callable, Union, Optional

from gbvision.constants.types import Frame, Shape
from gbvision.utils.continuity import ContinuesCircle
from gbvision.utils.continuity.continues_rect import ContinuesRect
from gbvision.utils.continuity import ContinuesRotatedRect
from gbvision.utils.continuity import ContinuesShape
from gbvision.utils.tracker import Tracker


class ContinuesShapeWrapper:
    """
    An object that tracks several shapes in a frame using continuity

    :param shapes: A list of shapes to track using continuity (must be of the same shape)
    :param frame: The frame from which the shapes were found
    :param finding_pipeline: A function that finds the shapes in a given frame and returns a list of them
                             (order irrelevant)
    :param shape_type: The type of the shape, can be either 'CIRCLE', 'RECT', or 'ROTATED_RECT', default is 'RECT',
                       can also be a class that inherits from ContinuesShape
    :param tracker_type: The type of the trackers to use, default is 'EMPTY'
    :param shape_lifespan: The maximum amount of frames for a shape to not be found until it is considered lost
    :param track_new: Indicates whether to track new shapes that were un-tracked so far or ignore them, default is False
                      (ignore)
    :param args: Additional arguments for continues shape constructor
    :param kwargs: Additional keyword arguments for continues shape constructor
    """

    SHAPE_TYPE_CIRCLE = 'CIRCLE'
    SHAPE_TYPE_RECT = 'RECT'
    SHAPE_TYPE_ROTATED_RECT = 'ROTATED_RECT'

    _CONTINUES_SHAPE_TYPES = {
        SHAPE_TYPE_CIRCLE: ContinuesCircle,
        SHAPE_TYPE_RECT: ContinuesRect,
        SHAPE_TYPE_ROTATED_RECT: ContinuesRotatedRect

    }

    def __init__(self, shapes: List[Shape], frame: Frame, finding_pipeline: Callable[[Frame], List[Shape]],
                 shape_type: Union[str, type] = SHAPE_TYPE_RECT, tracker_type: str = Tracker.TRACKER_TYPE_EMPTY,
                 shape_lifespan: Optional[int] = None, track_new: bool = False, *args, **kwargs):

        if shape_type in self._CONTINUES_SHAPE_TYPES:
            self.shape_type = self._CONTINUES_SHAPE_TYPES[shape_type]
        else:
            self.shape_type = shape_type
        self.tracker_type = tracker_type
        self.shape_lifespan = shape_lifespan
        self.finding_pipeline = finding_pipeline
        self.shapes: Dict[int, ContinuesShape] = {}
        self.track_new = track_new
        self.__args = args
        self.__kwargs = kwargs
        for i, shape in enumerate(shapes):
            self.shapes[i] = self.__create_continues_shape(shape, frame)
        self.__idx = len(shapes)

    def __create_continues_shape(self, shape, frame) -> ContinuesShape:
        return self.shape_type(shape, frame, Tracker(self.tracker_type), *self.__args, **self.__kwargs)

    def find_shapes(self, frame: Frame) -> Dict[int, Shape]:
        """
        Finds all shapes in the frame, them performs a continues shape operations on them and return the result as a dict where the keys are unique ids and the values are the shapes
        if a shape was lost it removes it from the tracked shapes list
        if a new shape was found and the track_new field is set to True it adds it to the tracked shapes list

        :param frame: The frame to search in
        :return: A dict mapping from unique ids to shapes, based on continuity
        """
        shapes = self.finding_pipeline(frame)
        result = {}
        to_delete = []
        for i in self.shapes:
            cont_shape = self.shapes[i]
            if cont_shape.is_lost(self.shape_lifespan):
                to_delete.append(i)
                continue
            found = False
            for j, shape in enumerate(shapes):
                if cont_shape.update(shape, frame):
                    found = True
                    del shapes[j]
                    break
            if not found:
                cont_shape.update_forced(frame)
            result[i] = cont_shape.get()
        for i in to_delete:
            del self.shapes[i]
        if self.track_new:
            for shape in shapes:
                self.shapes[self.__idx] = self.__create_continues_shape(shape, frame)
                result[self.__idx] = self.shapes[self.__idx].get()
                self.__idx += 1
        return result

    def get_shapes(self) -> Dict[int, Shape]:
        """
        Returns the current location of the shapes based on continuity
        NOTE! this will be applied to the last frame given to the find_shapes method, only use this method if you need to get the shapes twice in an iteration

        :return: A dict mapping from unique ids to shapes
        """
        result = {}
        for i in self.shapes:
            result[i] = self.shapes[i].get()
        return result

    def get_shapes_as_list(self) -> List[Shape]:
        """
        Gets all the shapes as a list instead of a dictionary

        :return: A list of all the tracked shapes (sorted by unique id's)
        """
        return list(self.get_shapes().values())
