from typing import Any, List, Dict

from gbvision.constants.types import Frame
from gbvision.continuity.continues_circle import ContinuesCircle
from gbvision.continuity.continues_rect import ContinuesRect
from gbvision.continuity.continues_rotated_rect import ContinuesRotatedRect
from gbvision.continuity.continues_shape import ContinuesShape
from gbvision.utils.pipeline import PipeLine
from gbvision.utils.tracker import Tracker

_CONTINUES_SHAPE_TYPES = {
    'CIRCLE': ContinuesCircle,
    'RECT': ContinuesRect,
    'ROTATED_RECT': ContinuesRotatedRect

}


class ContinuesShapeWrapper:
    def __init__(self, shapes: List[Any], frame: Frame, finding_pipeline: PipeLine, stype='RECT', tracker_type='EMPTY',
                 shape_lifespam: int = None, track_new=False, *args, **kwargs):
        self.stype = stype.upper()
        assert self.stype in _CONTINUES_SHAPE_TYPES
        self.tracker_type = tracker_type
        self.shape_lifespam = shape_lifespam
        self.finding_pipeline = finding_pipeline
        self.shapes: Dict[int, ContinuesShape] = {}
        self.track_new = track_new
        self.__args = args
        self.__kwargs = kwargs
        for i, shape in enumerate(shapes):
            self.shapes[i] = self.__create_continues_shape(shape, frame)
        self.__idx = len(shapes)

    def __create_continues_shape(self, shape, frame) -> ContinuesShape:
        return _CONTINUES_SHAPE_TYPES[self.stype](shape, frame, Tracker(self.tracker_type), *self.__args,
                                                  **self.__kwargs)

    def find_shapes(self, frame: Frame) -> Dict[int, Any]:
        """
        finds all shapes in the frame, them performs a continues shape operations on them and return the result as a dict where the keys are unique ids and the values are the shapes
        if a shape was lost it removes it from the tracked shapes list
        if a new shape was found and the track_new field is set to True it adds it to the tracked shapes list

        :param frame: the frame to search in
        :return: a dict mapping from unique ids to shapes, based on continuity
        """
        shapes = self.finding_pipeline(frame)
        result = {}
        for i in self.shapes:
            cont_shape = self.shapes[i]
            if cont_shape.is_lost(self.shape_lifespam):
                del self.shapes[i]
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
        if self.track_new:
            for shape in shapes:
                self.shapes[self.__idx] = self.__create_continues_shape(shape, frame)
                result[self.__idx] = self.shapes[self.__idx].get()
                self.__idx += 1
        return result

    def get_shapes(self):
        """
        returns the current location of the shapes based on continuity
        NOTE! this will be applied to the last frame given to the find_shapes method, only use this method if you need to get the shapes twice in an iteration

        :return:
        """
        result = {}
        for i in self.shapes:
            result[i] = self.shapes[i].get()
        return result


    def get_shapes_as_list(self):
        return list(self.get_shapes().values())
