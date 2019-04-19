import cv2
import numpy as np

from gbvision.utils.pipeline import PipeLine


def erode(ksize: int or (int, int), iterations=1):
    """
    creates a pipeline that erodes the image by a kernel of ones
    used mainly for erode & dilate denoise filters
    :param ksize: the kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
    :param iterations: optional, the amount of erode iterations to perform, default is 1
    None! a large number of iterations will slow down the program
    :return: a pipeline that erodes the given frame
    """
    if type(ksize) is int:
        ksize = (ksize, ksize)
    return PipeLine(lambda frame: cv2.erode(frame, np.ones(ksize), iterations=iterations))


def dilate(ksize: int or (int, int), iterations=1):
    """
    creates a pipeline that dilates the image by a kernel of ones
    used mainly for erode & dilate denoise filters
    :param ksize: the kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
    :param iterations: optional, the amount of dilate iterations to perform, default is 1
    None! a large number of iterations will slow down the program
    :return: a pipeline that dilates the given frame
    """
    if type(ksize) is int:
        ksize = (ksize, ksize)
    return PipeLine(lambda frame: cv2.dilate(frame, np.ones(ksize), iterations=iterations))


def median_blur(ksize: int):
    """
    creates a pipeline that blurs the given frame using the median blur method
    works very good for denoising purposes
    :param ksize: the size of the kernel used by the filter, must be an odd number
    :return: a pipeline that filters the image using the median blur method
    """
    return PipeLine(lambda frame: cv2.medianBlur(frame, ksize))
