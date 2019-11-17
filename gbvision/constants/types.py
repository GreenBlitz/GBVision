from typing import Tuple, List, Union
from numpy import ndarray

Number = Union[int, float]
Point = Tuple[Number, Number]  # (x, y)
NoneType = type(None)
Contour = ndarray
Circle = Tuple[Tuple[Number, Number], Number]  # ((center_x, center_y), radius)
Rect = Tuple[Number, Number, Number, Number]  # (x, y, width, height)
Polygon = Contour
FixedPolygon = List[Point]
RotatedRect = Tuple[Point, Point, float]  # ((x1, y1), (x2, y2), angle)
Ellipse = RotatedRect
Frame = Union[ndarray, NoneType]
Color = Tuple[int, int, int]
