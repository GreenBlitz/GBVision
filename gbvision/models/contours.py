from typing import List

import cv2

from gbvision.constants.math import EPSILON
from gbvision.constants.system import CONTOURS_INDEX
from gbvision.constants.types import Contour, Polygon, Point, Frame
from gbvision.utils.pipeline import PipeLine


def __mapper(func) -> PipeLine:
    return PipeLine(lambda x: list(map(func, x)))


@PipeLine
def find_contours(frame: Frame) -> List[Contour]:
    """
    finds the contours in a binary frame

    :param frame: the frame (usually after threshold and denoising)
    :return: a list of all the contours in the frame
    """
    # DO NOT CHANGE THE CHAIN_APPROX_NONE
    # You do not know the damages it may cause
    return cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[CONTOURS_INDEX]


@PipeLine
def sort_contours(cnts: List[Contour]) -> List[Contour]:
    """
    sorts the list of contours by the contour area

    :param cnts: the list of contours
    :return: the list given, sorted by area
    """
    return sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)


class FilterContours(PipeLine):
    """
    a pipeline factory that receives a list of contours and filters out all contours with an area less then defined
    to the pipeline

    :param min_area: the minimal area of a contour in order for it to pass the filter
    """
    def __init__(self, min_area: float):
        PipeLine.__init__(self, lambda cnts: filter(lambda c: cv2.contourArea(c) >= min_area, cnts), list)


convex_hull = PipeLine(cv2.convexHull)

convex_hull_multiple = __mapper(convex_hull)


@PipeLine
def contour_center(cnt: Contour) -> Point:
    """
    finds the center of the contour
    :param cnt: a contour object
    :return: the center of the contour object
    """
    m = cv2.moments(cnt)
    return int(m['m10'] / (m['m00'] + EPSILON)), int(m['m01'] / (m['m00'] + EPSILON))


contours_centers = __mapper(contour_center)

# SHAPES

contours_to_rects = __mapper(cv2.boundingRect)


@PipeLine
def sort_rects(rects):
    return list(sorted(rects, key=lambda x: x[2] * x[3], reverse=True))


contours_to_rects_sorted = contours_to_rects + sort_rects

contours_to_circles = __mapper(cv2.minEnclosingCircle)


@PipeLine
def sort_circles(circs):
    return list(sorted(circs, key=lambda x: x[1], reverse=True))


contours_to_circles_sorted = contours_to_circles + sort_circles

contours_to_rotated_rects = __mapper(cv2.minAreaRect)


@PipeLine
def sort_rotated_rects(rects):
    return list(sorted(rects, key=lambda x: x[1][0] * x[1][1], reverse=True))


contours_to_rotated_rects_sorted = contours_to_rotated_rects + sort_rotated_rects


@PipeLine
def contours_to_ellipses(cnts):
    cnts = filter(lambda x: len(x) >= 5, cnts)
    # ellipse must get contours of at least five points
    return list(map(cv2.fitEllipse, cnts))


sort_ellipses = sort_rotated_rects

contours_to_ellipses_sorted = contours_to_ellipses + sort_ellipses


@PipeLine
def contours_to_polygons(cnts):
    """
    performs approxPolyDP algorithm on a list of contours

    :param cnts: the list of contours
    :return: a list of polygons from the contours
    """
    arc_lengts = map(lambda cnt: 0.05 * cv2.arcLength(cnt, True), cnts)
    return list(map(lambda cnt: cv2.approxPolyDP(cnt, next(arc_lengts), True), cnts))


@PipeLine
def fix_contours_shape(cnts: List[Contour]) -> List[Polygon]:
    """
    fixes the contours to a usable shape
    the shape of the contours is a list of tuples of integers/floats, where each tuple is a point
    an example of two rectangles represented with this shape will be:
    [[(0, 0), (0, 2), (1, 2), (1, 0)],
    [(5, 4), (7, 4), (7, 9), (9, 5)]]
    
    :param cnts: the contours / polygons list whose shape should be fixed
    :return: a list of all the contours with the fixed shape
    """
    cnts = map(lambda polydp: map(lambda x: x[0], polydp), cnts)
    return list(map(lambda polydp: list(map(tuple, polydp)), cnts))


sort_polygons = sort_contours

polygon_center = contour_center

polygons_centers = contours_centers
