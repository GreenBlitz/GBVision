from typing import Union, Tuple
import cv2
import numpy as np

from gbvision.utils.pipeline import PipeLine


class Dilate(PipeLine):
    """
    creates a pipeline that dilates the image by a kernel of ones
    used mainly for Erode & Dilate denoise filters

    :param ksize: The kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
    :param iterations: Optional. The amount of Dilate iterations to perform, default is 1.
                       Note! A large number of iterations will slow down the program
    :return: A pipeline that dilates the given frame
    """

    def __init__(self, ksize: Union[int, Tuple[int, int]], iterations=1):
        if type(ksize) is int:
            ksize = (ksize, ksize)
        PipeLine.__init__(self, lambda frame: cv2.dilate(frame, np.ones(ksize), iterations=iterations))
