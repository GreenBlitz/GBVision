import cv2
import numpy as np

from gbvision.constants.types import Frame
from gbvision.utils.pipeline import PipeLine


@PipeLine
def corners(frame: Frame) -> Frame:
    """
    Corner finding by a laplacian convolution of the frame by the matrix:
        [-1 1]
        [1 -1]

    :param frame: the frame to convolve
    :return: the convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[-1, 1], [1, -1]]))


@PipeLine
def edges(frame: Frame) -> Frame:
    """
    Edges finding by the Canny algorithm

    :param frame: The frame to convolve
    :return: The convolved frame
    """
    return cv2.Canny(frame, 100, 200)


@PipeLine
def sharpen(frame: Frame) -> Frame:
    """
    Sharpens the frame by a laplacian convolution of the frame by the matrix:
        [-1 -1 -1]
        [-1 9 -1]
        [-1 -1 -1]

    :param frame: The frame to convolve
    :return: The convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


@PipeLine
def blur(frame: Frame) -> Frame:
    """
    Blurs the frame by a laplacian convolution of the frame by the matrix:
        [1/9 1/9 1/9]
        [1/9 1/9 1/9]
        [1/9 1/9 1/9]

    :param frame: The frame to convolve
    :return: The convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9)


@PipeLine
def blue(frame: Frame) -> Frame:
    """
    Gets the blue channel of the frame

    :param frame: The frame
    :return: The blue channel only (as a grayscale frame)
    """
    return frame[:, :, 0]


@PipeLine
def green(frame: Frame) -> Frame:
    """
    Gets the green channel of the frame

    :param frame: The frame
    :return: The green channel only (as a grayscale frame)
    """
    return frame[:, :, 1]


@PipeLine
def red(frame: Frame) -> Frame:
    """
    Gets the red channel of the frame

    :param frame: The frame
    :return: The red channel only (as a grayscale frame)
    """
    return frame[:, :, 2]


@PipeLine
def gray(frame: Frame) -> Frame:
    """
    Turns the frame to grayscale

    :param frame: The frame
    :return: The frame in grayscale form
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


@PipeLine
def normalize(frame: Frame) -> Frame:
    """
    Normalizes the frame to a pixel range of 0-1
    Equivalent to (frame - min(frame)) / max(abs(frame - min(frame)))

    :param frame: The frame
    :return: The normalized frame (data type float32)
    """
    return cv2.normalize(frame, None, alpha=0.0, beta=1.0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)


@PipeLine
def distance_transform(frame: Frame) -> Frame:
    """
    Performs the distance transform algorithm on a binary frame

    :param frame: The frame (binary, usually after threshold)
    :return: The distance transform of the frame using euclidean distance method
    """
    return cv2.distanceTransform(frame, cv2.DIST_L2, 3)


normalized_distance_transform = distance_transform + normalize
