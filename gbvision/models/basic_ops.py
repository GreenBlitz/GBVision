import cv2
import numpy as np

from gbvision.utils import PipeLine


def _corners(im):
    return cv2.filter2D(im, -1, np.array([[-1, 1], [1, -1]]))


corners = PipeLine(_corners)


def _edges(im):
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]))


edges = PipeLine(_edges)


def _sharpen(im):
    return cv2.filter2D(im, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


sharpen = PipeLine(_sharpen)


def _blur(im):
    return cv2.filter2D(im, -1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9)


blur = PipeLine(_blur)


def _blue(im):
    return im[:, :, 0]


blue = PipeLine(_blue)


def _green(im):
    return im[:, :, 1]


green = PipeLine(_green)


def _red(im):
    return im[:, :, 2]


red = PipeLine(_red)


def _gray(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)


gray = PipeLine(_gray)


