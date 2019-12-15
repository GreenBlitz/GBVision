from typing import Union, Tuple
import cv2
import numpy as np

from gbvision.constants.system import EMPTY_PIPELINE
from gbvision.models.contours import FilterContours, find_contours
from gbvision.thresholds.threshold import Threshold
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

class GrabCut(PipeLine):
    """
        creates a pipeline that finds objects of intrest in frame using the GrabCut

        :param ksize: the size of the kernel used by the filter, must be an odd number
        :return: a pipeline that filters the image using the median blur method
        """


    def __init__(self, threshold: Threshold, contour_min_area=0.0):
        self.threshold_val = EMPTY_PIPELINE + threshold + find_contours + FilterContours(contour_min_area)
        PipeLine.__init__(self, lambda frame: self.filter_frame(frame))


    def filter_frame(self, frame):
        thresh = self.threshold_val(frame)
        img = frame.copy()
        mask = np.zeros(img.shape[:2], np.uint8)

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        wid = img.shape[0]
        hei = img.shape[1]

        rect = (20, 20, 60, 60)
        # cv2.rectangle(img, (int(0.45 * wid), int(0.45 * hei)), (int(0.65 * wid), int(0.65 * hei)), (255, 0, 0), 5)
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 8, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

        img = img * mask2[:, :, np.newaxis]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (0, 0), fx=4, fy=4)
        ctrs = gbv.find_contours(gray)

        frame = cv2.resize(frame, (0, 0), fx=4, fy=4)
        cv2.drawContours(frame, ctrs, 0, (0, 255, 0), 3)
        cv2.imshow("stream", frame)

