import cv2

from gbvision.constants.math import EPSILON
from gbvision.constants.system import CONTOURS_INDEX
from gbvision.utils.pipeline import PipeLine


@PipeLine
def find_contours(frame):
    return cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[CONTOURS_INDEX]


@PipeLine
def sort_contours(cnts):
    return sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True)


class FilterContours(PipeLine):
    def __init__(self, min_area: float):
        PipeLine.__init__(self, lambda cnts: filter(lambda c: cv2.contourArea(c) >= min_area, cnts), list)


convex_hull = PipeLine(cv2.convexHull)


@PipeLine
def convex_hull_multiple(cnts):
    return list(map(convex_hull, cnts))


@PipeLine
def contour_center(cnt):
    m = cv2.moments(cnt)
    return int(m['m10'] / (m['m00'] + EPSILON)), int(m['m01'] / (m['m00'] + EPSILON))

@PipeLine
def contours_centers(cnts):
    return list(map(contour_center, cnts))

# SHAPES

@PipeLine
def contours_to_rects(cnts):
    return list(map(cv2.boundingRect, cnts))

@PipeLine
def sort_rects(rects):
    return list(sorted(rects, key=lambda x: x[2] * x[3], reverse=True))

contours_to_rects_sorted = contours_to_rects + sort_rects

@PipeLine
def contours_to_circles(cnts):
    return list(map(cv2.minEnclosingCircle, cnts))

@PipeLine
def sort_circles(circs):
    return list(sorted(circs, key=lambda x: x[1], reverse=True))

contours_to_circles_sorted = contours_to_circles + sort_circles

@PipeLine
def contours_to_rotated_rects(cnts):
    return list(map(cv2.minAreaRect, cnts))

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
    arc_lengts = map(lambda cnt: 0.05 * cv2.arcLength(cnt, True), cnts)
    return list(map(lambda cnt: cv2.approxPolyDP(cnt, next(arc_lengts), True), cnts))

sort_polygons = sort_contours

polygon_center = contour_center

polygons_centers = contours_centers


