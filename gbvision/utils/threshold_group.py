import sys
from functools import reduce

import cv2


class ThresholdGroup:
    """
    a class that constructs a threshold filter out of several threshold filters and a binary mask function
    for example, use of the function on two thresholds with the binary function "bitwise_or" will result
    in a filter that outputs 255 for a pixel if it is in either one of the threshold's range
    using the "bitwise_and" function will output 255 for a pixel only if it is in both the threshold's range
    """

    def __init__(self, *thresholds, **kwargs):
        """
        initializes the threshold group
        :param thresholds: all the thresholds to join in the threshold group
        :param binary_mask: a binary function that maps from a pair of binary images to a single binary image
        default value is cv2.bitwise_or
        :param default_pixel: the default value of a pixel before the threshold function
        when using the 'bitwise_or' function this should be initialized to 0, when using cv2.bitwise_and this should be
        initialized to 255
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

    def __call__(self, frame):
        """
        apply the threshold filter to the frame
        :param frame: the frame to apply the filter to
        :return: the binary image, the frame after the threshold group filter
        """
        return reduce(lambda th_frame, threshold: self.binary_mask(th_frame, threshold(frame)), self.thresholds,
                      self.default_pixel)

    def __add__(self, other):
        """
        adds another threshold to the group and returns the new threshold group
        :param other: a threshold function ,can be a threshold, threshold group, or any type of function
        :return: a new threshold group with the other threshold joined
        """
        return ThresholdGroup(self.thresholds + [other], binary_mask=self.binary_mask, default_pixel=self.default_pixel)

    def __iadd__(self, other):
        """
        adds a new threshold filter to this threshold group
        :param other: a threshold function ,can be a threshold, threshold group, or any type of function
        """
        self.thresholds += [other]

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

    def __getitem__(self, item):
        return self.thresholds[item]

    def __setitem__(self, key, value):
        self.thresholds[key] = value
