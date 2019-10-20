from typing import List

from gbvision.constants.types import RotatedRect, Polygon, Rect, Circle
from gbvision.utils.pipeline import PipeLine
import numpy as np
import cv2


def circle_collision(circ1: Circle, circ2: Circle) -> bool:
    center1, r1 = circ1
    center2, r2 = circ2
    return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2 < (r1 + r2) ** 2


@PipeLine
def filter_inner_circles(circles: List[Circle]) -> List[Circle]:
    filtered_circles = []
    for i, circle in enumerate(circles):
        circle_invalid = False
        for j in range(i):
            circle_invalid = circle_collision(circle, circles[j])
            if circle_invalid:
                break
        if not circle_invalid:
            filtered_circles.append(circle)

    return filtered_circles


def rect_collision(r1: Rect, r2: Rect) -> bool:
    return not (r1[0] > r2[0] + r2[2] or
                r1[0] + r1[2] < r1[0] or
                r1[1] > r2[1] + r2[3] or
                r1[1] + r1[3] < r2[1])


@PipeLine
def filter_inner_rects(rects: List[Rect]) -> List[Rect]:
    filtered_rects = []
    for i, rect in enumerate(rects):
        rect_invalid = False
        for j in range(i):
            rect_invalid = rect_collision(rect, rects[j])
            if rect_invalid:
                break
        if not rect_invalid:
            filtered_rects.append(rect)
    return filtered_rects


def convex_shape_collision(shape1: Polygon, shape2: Polygon) -> bool:
    """
    detects collision between two convex shapes
    Note: if you are uncertain if a shape is convex, use convex_hull on it, it will make it convex
    
    :param shape1: the first shape, as a contour
    :param shape2: the second shape, as a contour
    :return:
    """
    for shape in [shape1, shape2]:
        for idx, edge1 in enumerate(shape):
            edge2 = shape[idx % len(shape1)]

            normal = (edge1 - edge2)[::-1].T
            normal[0] = -normal[0]

            min_1 = max_1 = None
            for edge in shape1:
                projected = edge.dot(normal)[0, 0]
                if min_1 is None or projected < min_1:
                    min_1 = projected

                if max_1 is None or projected > max_1:
                    max_1 = projected

            min_2 = max_2 = None
            for edge in shape2:
                projected = edge.dot(normal)[0, 0]
                if min_2 is None or projected < min_2:
                    min_2 = projected

                if max_2 is None or projected > max_2:
                    max_2 = projected

            if max_1 < min_2 or max_2 < min_1:
                return False

    return True


@PipeLine
def filter_inner_convex_shapes(shapes: List[Polygon]) -> List[Polygon]:
    filtered_shapes = []
    for i, shape in enumerate(shapes):
        shape_invalid = False
        for j in range(i):
            shape_invalid = convex_shape_collision(shape, shapes[j])
            if shape_invalid:
                break
        if not shape_invalid:
            filtered_shapes.append(shape)
    return filtered_shapes


def rotated_rect_collision(rr1: RotatedRect, rr2: RotatedRect) -> bool:
    return convex_shape_collision(np.array([cv2.boxPoints(rr1)]), np.array([cv2.boxPoints(rr2)]))


@PipeLine
def filter_inner_rotated_rects(rotated_rects: List[RotatedRect]) -> List[RotatedRect]:
    filtered_rotated_rects = []
    for i, rotated_rect in enumerate(rotated_rects):
        rotated_rect_invalid = False
        for j in range(i):
            rotated_rect_invalid = rotated_rect_collision(rotated_rect, rotated_rects[j])
            if rotated_rect_invalid:
                break
        if not rotated_rect_invalid:
            filtered_rotated_rects.append(rotated_rect)
    return filtered_rotated_rects
