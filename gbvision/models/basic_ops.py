import cv2
import numpy as np

from gbvision.utils.pipeline import PipeLine


@PipeLine
def corners(frame):
    return cv2.filter2D(frame, -1, np.array([[-1, 1], [1, -1]]))


@PipeLine
def edges(frame):
    return cv2.filter2D(frame, -1, np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]))


@PipeLine
def sharpen(frame):
    return cv2.filter2D(frame, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


@PipeLine
def blur(frame):
    return cv2.filter2D(frame, -1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9)


@PipeLine
def blue(frame):
    return frame[:, :, 0]


@PipeLine
def green(frame):
    return frame[:, :, 1]


@PipeLine
def red(frame):
    return frame[:, :, 2]


@PipeLine
def gray(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
