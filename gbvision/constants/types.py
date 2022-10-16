from typing import Tuple, List, Union, Callable, TypeVar, Optional, Any
from numpy import ndarray

Number = Union[int, float]
Point = Tuple[Number, Number]  # (x, y)
Contour = ndarray  # [[x0, y0], [x1, y1], ... ]
Circle = Tuple[Tuple[Number, Number], Number]  # ((center_x, center_y), radius)
Rect = Tuple[Number, Number, Number, Number]  # (x, y, width, height)
Polygon = Union[List[Point], Contour]
FixedPolygon = List[Point]
RotatedRect = Tuple[Point, Point, float]  # ((center_x, center_y), (width, height), angle in degrees)
Ellipse = RotatedRect
Frame = Optional[ndarray]
Color = Tuple[int, int, int]
FilterFunction = Callable[[Frame], Frame]
Coordinates = Tuple[int, int]  # (x, y)
Line = Tuple[Point, Point]
Location = Union[Tuple[Number, Number, Number], ndarray]
ROI = Tuple[int, int, int, int]  # (x, y, width, height)
Shape = TypeVar('Shape')
ColorThresholdParams = Tuple[Tuple[Number, Number], Tuple[Number, Number], Tuple[Number, Number]]
# ((channel0 low, channel0 high), (channel1 low, channel1 high), (channel2 low, channel2 high))
GrayScaleThresholdParams = Tuple[Number, Number]  # (low, high)

try:
    from typing import Protocol


    class TrackerType(Protocol):
        init: Callable[[Frame, Rect], bool]
        update: Callable[[Frame], Tuple[bool, Rect]]
except ImportError:
    # Protocol is not supported in python 3.7
    TrackerType = Any
