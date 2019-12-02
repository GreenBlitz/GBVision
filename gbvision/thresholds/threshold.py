import abc
from collections import Iterator
from functools import reduce

import cv2
from traitlets import Any

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
    def __call__(self, frame: Frame) -> Frame:
        """
        activates the threshold filter on the given image
        :param frame: the image to activate the threshold on
        :return: a binary image, the frame after the threshold filter
        """

    def __or__(self, other: FilterFunction) -> FilterFunction:
        return ThresholdGroup(self, other, binary_mask=cv2.bitwise_or, default_pixel=0)

    def __and__(self, other: FilterFunction) -> FilterFunction:
        return ThresholdGroup(self, other, binary_mask=cv2.bitwise_and, default_pixel=0xFF)


class ThresholdGroup(Threshold):
    """
    a class that constructs a threshold filter out of several threshold filters and a binary mask function
    for example, use of the function on two thresholds with the binary function "bitwise_or" will result
    in a filter that outputs 255 for a pixel if it is in either one of the threshold's range
    using the "bitwise_and" function will output 255 for a pixel only if it is in both the threshold's range

    :param thresholds: all the thresholds to join in the threshold group
    :param binary_mask: a binary function that maps from a pair of binary images to a single binary image
        default value is cv2.bitwise_or
    :param default_pixel: the default value of a pixel before the threshold function
        when using the 'bitwise_or' function this should be initialized to 0, when using cv2.bitwise_and this should be
        initialized to 255
    """

    def __init__(self, *thresholds: FilterFunction, **kwargs):
        """
        initializes the threshold group

        """
        self.binary_mask = cv2.bitwise_or
        self.default_pixel = 0
        if 'binary_mask' in kwargs:
            self.binary_mask = kwargs['binary_mask']
            del kwargs['binary_mask']
        if 'default_pixel' in kwargs:
            self.default_pixel = kwargs['default_pixel']
            del kwargs['default_pixel']
        for i in kwargs:
            print('[WARN] keyword value %s is never used' % i, file=sys.stderr)
        self.thresholds = list(thresholds)

    def __call__(self, frame: Frame) -> Frame:
        """
        apply the threshold filter to the frame
        :param frame: the frame to apply the filter to
        :return: the binary image, the frame after the threshold group filter
        """
        return reduce(lambda th_frame, threshold: self.binary_mask(th_frame, threshold(frame)), self.thresholds,
                      self.default_pixel)

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
