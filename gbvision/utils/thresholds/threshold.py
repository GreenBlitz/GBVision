import abc
from typing import List, Callable

import cv2
import numpy as np
from gbvision.constants.math import EPSILON

from gbvision.constants.types import FilterFunction, Frame


class Threshold(abc.ABC):
    """
    a class that represents a function that maps from an image to a binary image
    where 255 states that the pixel at the original image was in a range represented by the threshold object
    and 0 states the pixel was out of the range
    for example:
    ColorThreshold([[200, 255], [0, 50], [0, 50]], 'RGB')
    the above threshold represents a relatively red pixel. when an image is filtered by it, every pixel that is
    relatively red will be given the value 255, and every pixel that isn't will be given the value of 0
    """

    @abc.abstractmethod
    def _threshold(self, frame: Frame) -> Frame:
        """
        unsafely activates the threshold filter on the given image
        :param frame: the image to activate the threshold on
        :return: a binary image, the frame after the threshold filter
        """

    def __call__(self, frame: Frame) -> Frame:
        frame = self._threshold(frame)
        if frame.dtype == np.uint8:
            return frame
        frame *= 255.0 / (np.max(frame) + EPSILON)
        return frame.astype(np.uint8)

    def __or__(self, other: 'Threshold') -> 'Threshold':
        return ThresholdGroup(cv2.bitwise_or, self, other)

    def __and__(self, other: 'Threshold') -> 'Threshold':
        return ThresholdGroup(cv2.bitwise_and, self, other)


class ThresholdGroup(Threshold):
    """
    a class that constructs a threshold filter out of several threshold filters and a binary mask function
    for example, use of the function on two thresholds with the binary function "bitwise_or" will result
    in a filter that outputs 255 for a pixel if it is in either one of the threshold's range
    using the "bitwise_and" function will output 255 for a pixel only if it is in both the threshold's range

    :param thresholds: all the thresholds to join in the threshold group
    :param binary_mask: a binary function that maps from a pair of binary images to a single binary image
        default value is cv2.bitwise_or
    """

    def __init__(self, binary_mask: Callable[[Frame, Frame], Frame], *thresholds):
        self.binary_mask = binary_mask
        self.thresholds: List[Threshold] = list(thresholds)

    def _threshold(self, frame: Frame) -> Frame:
        """
        apply the threshold filter to the frame
        :param frame: the frame to apply the filter to
        :return: the binary image, the frame after the threshold group filter
        """
        if len(self.thresholds) == 0:
            return frame
        frame_tag = self.thresholds[0](frame)
        for i in range(1, len(self.thresholds)):
            frame_tag = self.binary_mask(frame_tag, self.thresholds[i](frame))
        return frame_tag

    def __iter__(self):
        """
        :return: an iterator that iterates through all this group's filters
        """
        return iter(self.thresholds)

    def __len__(self):
        """
        :return: the amount of filters in this threshold group
        """
        return len(self.thresholds)

    def __getitem__(self, item: int) -> FilterFunction:
        return self.thresholds[item]

    def __setitem__(self, key: int, value: FilterFunction):
        self.thresholds[key] = value
