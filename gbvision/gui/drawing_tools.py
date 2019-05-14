import cv2
import numpy as np

from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.models.contours import find_contours, contours_to_circles, contours_to_rects, contours_to_rotated_rects,\
    contours_to_ellipses
from gbvision.utils.pipeline import PipeLine


class DrawContours(PipeLine):
    def __init__(self, threshold_func, color, thickness=2, contours_process=EMPTY_PIPELINE):
        contour_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process

        def _draw(frame):
            frame = frame.copy()
            cnts = contour_finding(frame)
            cv2.drawContours(frame, cnts, -1, color, thickness)
            return frame

        PipeLine.__init__(self, _draw)


class DrawCircles(PipeLine):
    def __init__(self, threshold_func, color, thickness=2, contours_process=EMPTY_PIPELINE,
                circle_process=EMPTY_PIPELINE):
        circle_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_circles + \
                         circle_process

        def _draw(frame):
            frame = frame.copy()
            circs = circle_finding(frame)
            for c in circs:
                cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), color, thickness)
            return frame

        PipeLine.__init__(self, _draw)


class DrawRects(PipeLine):
    def __init__(self, threshold_func, color, thickness=2, contours_process=EMPTY_PIPELINE,
              rects_process=EMPTY_PIPELINE):
        rect_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_rects + \
                       rects_process

        def _draw(frame):
            frame = frame.copy()
            rects = rect_finding(frame)
            for r in rects:
                cv2.rectangle(frame, (int(r[0]), int(r[1])), (int(r[0] + r[2]), int(r[1] + r[3])), color, thickness)
            return frame

        PipeLine.__init__(self, _draw)


class DrawRotatedRects(PipeLine):
    def __init__(self, threshold_func, color, thickness=2, contours_process=EMPTY_PIPELINE,
                     rotated_rects_process=EMPTY_PIPELINE):
        rotated_rect_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_rotated_rects + \
                               rotated_rects_process

        def _draw(frame):
            frame = frame.copy()
            rotated_rects = rotated_rect_finding(frame)
            for r in rotated_rects:
                box = cv2.boxPoints(r)
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, color, thickness)
            return frame

        PipeLine.__init__(self, _draw)


class DrawEllipses(PipeLine):
    def __init__(self, threshold_func, color, thickness=2, contours_process=EMPTY_PIPELINE,
                 ellipses_process=EMPTY_PIPELINE):
        ellipses_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_ellipses + \
                               ellipses_process

        def _draw(frame):
            frame = frame.copy()
            ellipses = ellipses_finding(frame)
            for e in ellipses:
                cv2.ellipse(frame, e, color, thickness)
            return frame

        PipeLine.__init__(self, _draw)
