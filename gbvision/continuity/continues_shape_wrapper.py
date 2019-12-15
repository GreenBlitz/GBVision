from typing import Any, List, Dict

from gbvision.constants.types import Frame
from gbvision.continuity.continues_circle import ContinuesCircle
from gbvision.continuity.continues_rect import ContinuesRect
from gbvision.continuity.continues_rotated_rect import ContinuesRotatedRect
from gbvision.utils.pipeline import PipeLine
from gbvision.utils.tracker import Tracker

_CONTINUES_SHAPE_TYPES = {
    'CIRCLE': ContinuesCircle,
    'RECT': ContinuesRect,
    'ROTATED_RECT': ContinuesRotatedRect

}


class ContinuesShapeWrapper:
    def __init__(self, shapes: List[Any], frame: Frame, finding_pipeline: PipeLine, stype='RECT', tracker_type='EMPTY', shape_lifespam: int = None,
                 *args, **kwargs):
        self.stype = stype.upper()
        assert self.stype in _CONTINUES_SHAPE_TYPES
        self.tracker_type = tracker_type
        self.shape_lifespam = shape_lifespam
        self.finding_pipeline = finding_pipeline
        self.shapes = {}
        for i, shape in enumerate(shapes):
            self.shapes[i] = _CONTINUES_SHAPE_TYPES[self.stype](shape, frame, Tracker(tracker_type), *args, **kwargs)

    def track_shapes(self, frame: Frame) -> Dict[int, Any]:
        shapes = self.finding_pipeline(frame)
        result = {}
        for i in self.shapes:
            cont_shape = self.shapes[i]
            if cont_shape.is_lost(self.shape_lifespam):
                result[i] = None
                continue
            found = False
            for j, shape in enumerate(shapes):
                if cont_shape.update(shape, frame):
                    found = True
                    break
            if not found:
                cont_shape.update_forced(frame)
            result[i] = cont_shape.get()

        return result

    @staticmethod
    def remove_lost_shapes(shapes_dict: Dict[int, Any]) -> List[Any]:
        result = []
        for i in shapes_dict:
            if shapes_dict[i] is not None:
                result.append(shapes_dict[i])
        return result
