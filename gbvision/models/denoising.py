from typing import Union, Tuple
import cv2
import numpy as np

from gbvision.utils.pipeline import PipeLine


class Erode(PipeLine):
    """
    creates a pipeline that erodes the image by a kernel of ones
    used mainly for Erode & Dilate denoise filters

    :param ksize: the kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
    :param iterations: optional, the amount of Erode iterations to perform, default is 1
        None! a large number of iterations will slow down the program
    :return: a pipeline that erodes the given frame
    """

    def __init__(self, ksize: Union[int, Tuple[int, int]], iterations=1):
        if type(ksize) is int:
            ksize = (ksize, ksize)
        PipeLine.__init__(self, lambda frame: cv2.erode(frame, np.ones(ksize), iterations=iterations))


class Dilate(PipeLine):
    """
        creates a pipeline that dilates the image by a kernel of ones
        used mainly for Erode & Dilate denoise filters

        :param ksize: the kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
        :param iterations: optional, the amount of Dilate iterations to perform, default is 1
            None! a large number of iterations will slow down the program
        :return: a pipeline that dilates the given frame
        """

    def __init__(self, ksize: Union[int, Tuple[int, int]], iterations=1):
        if type(ksize) is int:
            ksize = (ksize, ksize)
        PipeLine.__init__(self, lambda frame: cv2.dilate(frame, np.ones(ksize), iterations=iterations))


class MedianBlur(PipeLine):
    """
    creates a pipeline that blurs the given frame using the median blur method
    works very good for denoising purposes

    :param ksize: the size of the kernel used by the filter, must be an odd number
    :return: a pipeline that filters the image using the median blur method
    """

    def __init__(self, ksize: int):
        PipeLine.__init__(self, lambda frame: cv2.medianBlur(frame, ksize))
