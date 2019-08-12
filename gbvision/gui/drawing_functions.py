import cv2
import numpy as np

def draw_contours(frame, cnts, color, *args, **kwargs):
    frame = frame.copy()
    cv2.drawContours(frame, cnts, -1, color, *args, **kwargs)
    return frame


def draw_circles(frame, circs, color, *args, **kwargs):
    frame = frame.copy()
    for c in circs:
        cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), color, *args, **kwargs)
    return frame


def draw_rects(frame, rects, color, *args, **kwargs):
    frame = frame.copy()
    for r in rects:
        cv2.rectangle(frame, (int(r[0]), int(r[1])), (int(r[0] + r[2]), int(r[1] + r[3])), color, *args, **kwargs)
    return frame

def draw_rotated_rects(frame, rotated_rects, color, *args, **kwargs):
    frame = frame.copy()
    for r in rotated_rects:
        box = cv2.boxPoints(r)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, color, *args, **kwargs)
    return frame


def draw_ellipses(frame, ellipses, color, *args, **kwargs):
    frame = frame.copy()
    for e in ellipses:
        cv2.ellipse(frame, e, color, *args, **kwargs)
    return frame