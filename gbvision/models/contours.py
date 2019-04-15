import cv2

from gbvision.constants.math import EPSILON
from gbvision.constants.system import CONTOURS_INDEX
from gbvision.utils.pipeline import PipeLine

find_contours = PipeLine(lambda frame: cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[CONTOURS_INDEX])

sort_contours = PipeLine(lambda cnts: sorted(cnts, key=lambda x: cv2.contourArea(x), reverse=True))


def filter_contours(min_area: float):
    return PipeLine((lambda cnts: filter(lambda c: cv2.contourArea(c) >= min_area, cnts))) + list


contour_center = PipeLine(lambda cnt: cv2.moments(cnt),
                          lambda m: (int(m['m10'] / (m['m00'] + EPSILON)), int(m['m01'] / (m['m00'] + EPSILON))))

contours_centers = PipeLine(lambda cnts: map(contour_center, cnts)) + list

# SHAPES

contours_to_rects = PipeLine(lambda cnts: map(cv2.boundingRect, cnts)) + list

contours_to_rects_sorted = contours_to_rects + (
    lambda rects: sorted(rects, key=lambda x: x[2] * x[3], reverse=True)) + list

contours_to_circles = PipeLine(lambda cnts: map(cv2.minEnclosingCircle, cnts)) + list

contours_to_circles_sorted = contours_to_circles + (
    lambda rects: sorted(rects, key=lambda x: x[1], reverse=True)) + list

contours_to_ellipses = PipeLine(lambda cnts: filter(lambda x: len(x) >= 5, cnts),
                                # ellipse must get contours of at least five points
                                lambda cnts: map(cv2.fitEllipse, cnts)) + list

contours_to_ellipses_sorted = contours_to_ellipses + (
    lambda elps: sorted(elps, key=lambda x: x[1][0] * x[1][1], reverse=True)) + list

contours_to_rotated_rects = PipeLine(lambda cnts: map(cv2.minAreaRect, cnts)) + list

contours_to_rotated_rects_sorted = contours_to_rotated_rects + PipeLine(
    lambda rects: sorted(rects, key=lambda x: x[1][0] * x[1][1])) + list

contours_to_polygons = PipeLine(lambda cnts: map(lambda cnt: (cnt, 0.05 * cv2.arcLength(cnt, True)), cnts),
                                lambda cnts: map(lambda cnt0_eps1: cv2.approxPolyDP(cnt0_eps1[0], cnt0_eps1[1], True),
                                                 cnts),
                                lambda polydps: map(lambda polydp: map(lambda x: x[0], polydp), polydps),
                                lambda polydps: map(lambda polydp: list(map(tuple, polydp)), polydps)) + list
