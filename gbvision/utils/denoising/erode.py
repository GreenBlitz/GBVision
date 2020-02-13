from typing import Union, Tuple
import cv2
import numpy as np

from gbvision.utils.pipeline import PipeLine


class Erode(PipeLine):
    """
    creates a pipeline that erodes the image by a kernel of ones
    used mainly for Erode & Dilate denoise filters

    :param ksize: the kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
    :param iterations: optional, the amount of Erode iterations to perform, default is 1.
        Note! a large number of iterations will slow down the program
    :return: a pipeline that erodes the given frame
    """

    def __init__(self, ksize: Union[int, Tuple[int, int]], iterations=1):
        if type(ksize) is int:
            ksize = (ksize, ksize)
        PipeLine.__init__(self, lambda frame: cv2.erode(frame, np.ones(ksize), iterations=iterations))
