from typing import List, Callable

from gbvision.constants.types import RotatedRect, Polygon, Rect, Circle, Shape
from gbvision.utils.pipeline import PipeLine
import numpy as np
import cv2


class __InnerShapeFilter(PipeLine):
    """
    filters out all the shapes that are colliding with shapes with a lower (smaller) index
    maps from List[Shape] to List[Shape], where the output list is the input list without the colliding shapes
    usually used on a sorted list, to remove any shape that is inside another shape

    """

    def __init__(self, collision_func: Callable[[Shape, Shape], bool]):
        def _filter(shapes: List[Shape]) -> List[Shape]:
            filtered_shapes = []
            for i, shape in enumerate(shapes):
                shape_invalid = False
                for j in range(i):
                    shape_invalid = collision_func(shape, shapes[j])
                    if shape_invalid:
                        break
                if not shape_invalid:
                    filtered_shapes.append(shape)
            return filtered_shapes

        PipeLine.__init__(self, _filter)


def circle_collision(circ1: Circle, circ2: Circle) -> bool:
    """
    detects if two circles are colliding

    :param circ1: the first circle
    :param circ2: the second circle
    :return: True if circles are colliding, False otherwise
    """
    center1, r1 = circ1
    center2, r2 = circ2
    return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2 < (r1 + r2) ** 2


filter_inner_circles = __InnerShapeFilter(circle_collision)


def rect_collision(r1: Rect, r2: Rect) -> bool:
    """
    detects if two rects are colliding

    :param r1: the first rect
    :param r2: the second rect
    :return: True if the rects are colliding, False otherwise
    """
    return not (r1[0] > r2[0] + r2[2] or
                r1[0] + r1[2] < r1[0] or
                r1[1] > r2[1] + r2[3] or
                r1[1] + r1[3] < r2[1])


filter_inner_rects = __InnerShapeFilter(rect_collision)


def convex_shape_collision(shape1: Polygon, shape2: Polygon) -> bool:
    """
    detects collision between two convex shapes
    Note: if you are uncertain if a shape is convex, use convex_hull on it, it will make it convex

    :param shape1: the first shape, as a contour
    :param shape2: the second shape, as a contour
    :return: True if the shapes are colliding, False otherwise
    """
    shape1, shape2 = np.array(shape1), np.array(shape2)
    shape1 = shape1.reshape(shape1.size // 2, 2)
    shape2 = shape2.reshape(shape1.size // 2, 2)

    projection_axises = []

    negation_array = np.array([-1.0, 1.0])

    for i in range(len(shape1)):
        projection_axises.append(shape1[(i + 1) % len(shape1)] - shape1[i])
    for i in range(len(shape2)):
        projection_axises.append(shape2[(i + 1) % len(shape2)] - shape2[i])

    for i in range(len(projection_axises)):
        projection_axises[i] = projection_axises[i][::-1] * negation_array

    for axis in projection_axises:
        proj1 = []
        for vertix in shape1:
            proj1.append(vertix.dot(axis))
        proj1 = min(proj1), max(proj1)

        proj2 = []
        for vertix in shape2:
            proj2.append(vertix.dot(axis))
        proj2 = min(proj2), max(proj2)

        if proj1[0] > proj2[1] or proj2[0] > proj1[1]:
            return False

    return True


filter_inner_convex_shapes = __InnerShapeFilter(convex_shape_collision)


def rotated_rect_collision(rr1: RotatedRect, rr2: RotatedRect) -> bool:
    """
    detects if two rotated rects are colliding

    :param rr1: the first rotated rect
    :param rr2: the second rotated rect
    :return: True if the shapes are colliding, False otherwise
    """
    return convex_shape_collision(cv2.boxPoints(rr1), cv2.boxPoints(rr2))


filter_inner_rotated_rects = __InnerShapeFilter(rotated_rect_collision)
