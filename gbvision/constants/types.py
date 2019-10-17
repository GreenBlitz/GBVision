from typing import Tuple, List
from numpy import ndarray

Point = Tuple[float, float]  # (x, y)
Contour = ndarray
Circle = Tuple[Tuple[float, float], float]  # ((center_x, center_y), radius)
Rect = Tuple[float, float, float, float]  # (x, y, width, height)
Polygon = Contour
FixedPolygon = List[Point]
RotatedRect = Tuple[Point, Point, float]  # ((x1, y1), (x2, y2), angle)
Ellipse = RotatedRect
Frame = ndarray
Color = Tuple[int, int, int]
