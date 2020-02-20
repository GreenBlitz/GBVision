from typing import List

import cv2
import numpy as np

from gbvision.constants.types import Frame, Contour, Color, Circle, Rect, RotatedRect, Ellipse, Coordinates, Number, \
    Line


def draw_contours(frame: Frame, cnts: List[Contour], color: Color, *args, **kwargs) -> Frame:
    """
    draws all contours on a copy of the frame and returns the copy

    :param frame: the frame to draw on
    :param cnts: the contours to draw
    :param color: the color to draw in
    :param args: all extra args to opencv's  drawContours (for example thickness)
    :param kwargs: all extra keyword args to opencv's  drawContours (for example thickness)
    :return: a copy of the frame, after drawing
    """
    frame = frame.copy()
    cv2.drawContours(frame, cnts, -1, color, *args, **kwargs)
    return frame


def draw_circles(frame: Frame, circs: List[Circle], color: Color, *args, **kwargs) -> Frame:
    """
    draws all circles on a copy of the frame and returns the copy

    :param frame: the frame to draw on
    :param circs: the circles to draw
    :param color: the color to draw in
    :param args: all extra args to opencv's circle (for example thickness)
    :param kwargs: all extra keyword args to opencv's circle (for example thickness)
    :return: a copy of the frame, after drawing
    """
    frame = frame.copy()
    for c in circs:
        cv2.circle(frame, (int(c[0][0]), int(c[0][1])), int(c[1]), color, *args, **kwargs)
    return frame


def draw_rects(frame: Frame, rects: List[Rect], color: Color, *args, **kwargs) -> Frame:
    """
    draws all rects on a copy of the frame and returns the copy

    :param frame: the frame to draw on
    :param rects: the rects to draw
    :param color: the color to draw in
    :param args: all extra args to opencv's rectangle (for example thickness)
    :param kwargs: all extra keyword args to opencv's rectangle (for example thickness)
    :return: a copy of the frame, after drawing
    """
    frame = frame.copy()
    for r in rects:
        cv2.rectangle(frame, (int(r[0]), int(r[1])), (int(r[0] + r[2]), int(r[1] + r[3])), color, *args, **kwargs)
    return frame


def draw_rotated_rects(frame: Frame, rotated_rects: List[RotatedRect], color: Color, *args, **kwargs) -> Frame:
    """
    draws all rotated rects on a copy of the frame and returns the copy

    :param frame: the frame to draw on
    :param rotated_rects: the rotated rects to draw
    :param color: the color to draw in
    :param args: all extra args to opencv's drawContours (for example thickness)
    :param kwargs: all extra keyword args to opencv's drawContours (for example thickness)
    :return: a copy of the frame, after drawing
    """
    frame = frame.copy()
    for r in rotated_rects:
        box = cv2.boxPoints(r)
        box = np.int0(box)
        cv2.drawContours(frame, [box], 0, color, *args, **kwargs)
    return frame


def draw_ellipses(frame: Frame, ellipses: List[Ellipse], color: Color, *args, **kwargs) -> Frame:
    """
    draws all contours on a copy of the frame and returns the copy
    
    :param frame: the frame to draw on
    :param ellipses: the ellipses to draw
    :param color: the color to draw in
    :param args: all extra args to opencv's ellipse (for example thickness)
    :param kwargs: all extra keyword args to opencv's ellipse (for example thickness)
    :return: a copy of the frame, after drawing
    """
    frame = frame.copy()
    for e in ellipses:
        cv2.ellipse(frame, e, color, *args, **kwargs)
    return frame


def draw_lines(frame: Frame, lines: List[Line], color: Color, *args, **kwargs) -> Frame:
    """
    draws all Lines on a copy of the frame and returns the copy

    :param frame: the frame to draw on
    :param lines: the list of lines to draw
    :param color: the color to draw in
    :param args: all extra args to opencv's lines (for example thickness)
    :param kwargs: all extra keyword args to opencv's lines (for example thickness)
    :return: a copy of the frame, after drawing
    """

    frame = frame.copy()
    for line in lines:
        cv2.line(frame, line[0], line[1], color, *args, **kwargs)
    return frame


def draw_text(frame: Frame, text: str, coords: Coordinates, font_scale: Number, color: Color,
              font=cv2.FONT_HERSHEY_SIMPLEX, *args, **kwargs) -> Frame:
    """
    draws the text on a copy of the frame and returns the copy

    :param frame: the frame to draw on
    :param text: the text to draw
    :param coords: the coordinates of the bottom-left corner of the text
    :param font_scale: the size of the drawn text (multiplied by the default size of the font)
    :param color: the color to draw the text in
    :param font: the font, an opencv font constant, default is cv2.FONT_HERSHEY_SIMPLEX
    :param args: additional arguments to cv2.putText
    :param kwargs: additional keyword arguments to cv2.putText (such as thickness)
    :return: a copy of the frame with the text drawn on it
    """
    frame = frame.copy()
    cv2.putText(frame, text, coords, font, font_scale, color, *args, **kwargs)
    return frame
