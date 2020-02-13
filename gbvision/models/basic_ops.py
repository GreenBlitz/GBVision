import cv2
import numpy as np

from gbvision.utils.pipeline import PipeLine


@PipeLine
def corners(frame):
    """
    corner finding by a laplacian convolution of the frame by the matrix:
        [-1 1]
        [1 -1]

    :param frame: the frame to convolve
    :return: the convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[-1, 1], [1, -1]]))


@PipeLine
def edges(frame):
    """
    edges finding by a laplacian convolution of the frame by the matrix:
        [-1 -1 -1]
        [-1 8 -1]
        [-1 -1 -1]
    :param frame: the frame to convolve
    :return: the convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]))


@PipeLine
def sharpen(frame):
    """
    sharpens the frame by a laplacian convolution of the frame by the matrix:
        [-1 -1 -1]
        [-1 9 -1]
        [-1 -1 -1]

    :param frame: the frame to convolve
    :return: the convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]))


@PipeLine
def blur(frame):
    """
    blurs the frame by a laplacian convolution of the frame by the matrix:
        [1/9 1/9 1/9]
        [1/9 1/9 1/9]
        [1/9 1/9 1/9]

    :param frame: the frame to convolve
    :return: the convolved frame
    """
    return cv2.filter2D(frame, -1, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) / 9)


@PipeLine
def blue(frame):
    """
    gets the blue channel of the frame

    :param frame: the frame
    :return: the blue channel only (as a grayscale frame)
    """
    return frame[:, :, 0]


@PipeLine
def green(frame):
    """
    gets the green channel of the frame

    :param frame: the frame
    :return: the green channel only (as a grayscale frame)
    """
    return frame[:, :, 1]


@PipeLine
def red(frame):
    """
    gets the red channel of the frame

    :param frame: the frame
    :return: the red channel only (as a grayscale frame)
    """
    return frame[:, :, 2]


@PipeLine
def gray(frame):
    """
    turns the frame to grayscale

    :param frame: the frame
    :return: the frame in grayscale form
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


@PipeLine
def normalize(frame):
    """
    normalizes the frame to a pixel range of 0-1 or -1-1 (-1-1 only if there are already negative values in the frame).
    the normalization is done only by scalar multiplication, not by shifting values.
    equivalent to frame / max(abs(frame))

    :param frame: the frame
    :return: the normalized frame
    """
    return frame / np.max(abs(frame))


@PipeLine
def distance_transform(frame):
    """
    performs the distance transform algorithm on a binary frame

    :param frame: the frame (binary, usually after threshold)
    :return: the distance transform of the frame using euclidean distance method
    """
    return cv2.distanceTransform(frame, cv2.DIST_L2, 3)


normalized_distance_transform = distance_transform + normalize
