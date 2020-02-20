from typing import Union

import cv2
import numpy as np

from gbvision.constants.images import COLOR_TYPE
from gbvision.constants.types import Frame, Number, ROI
from gbvision.utils.thresholds import ColorThreshold
from gbvision.utils.thresholds.threshold import Threshold


def crop(frame: Frame, x: int, y: int, w: int, h: int) -> Frame:
    """
    crops the image from (x, y) to (x+w, y+h)

    :param frame: the frame to crop
    :param x: the x coordinate to crop from
    :param y: the y coordinate to crop from
    :param w: the width of the cropped image
    :param h: the height of the cropped image
    :return: the cropped image
    """
    return frame[y:y + h, x:x + w]


def median_threshold(frame: Frame, stdv: Union[Number, np.ndarray],
                     box: Union[None, ROI] = None, color_encoding=ColorThreshold.THRESH_TYPE_BGR) -> Threshold:
    """
    finds a threshold using the median threshold method
    the median threshold method defines the lower bounds of the threshold as the median of a given region of the image
    minus some deviation variable, and the upper bounds as the same median plus the deviation variable
    in a mathematical term, the threshold is defined to be [median(X) - V, median(X) + V] where X is the frame region
    and V is the deviation variable

    :param frame: the frame
    :param stdv: the deviation variable, can be a scalar (same deviation for every channel) or a numpy array with the
        same size as the number of channels in the threshold, the deviation will be defined for each channel separately
    :param box: optional, a sub region of the frame from which the median is calculated, when set to None the median is
        calculated from the entire frame
    :param color_encoding: the type of color encoding the threshold should use, default is BGR
    :return: a Threshold object
    """
    if box is not None:
        frame = crop(frame, *box)
    color_encoding = color_encoding.upper()
    if color_encoding != ColorThreshold.THRESH_TYPE_BGR:
        frame = cv2.cvtColor(frame, COLOR_TYPE[color_encoding])
    med = np.median(frame, axis=(0, 1)).astype(int)
    if type(med) is not np.ndarray:
        med = np.array([med])
    params = list(map(lambda x: list(map(int, x)),
                      np.vectorize(lambda x: min(255, max(0, x)))(np.array([med - stdv, med + stdv])).T))
    return ColorThreshold(params, color_encoding)
