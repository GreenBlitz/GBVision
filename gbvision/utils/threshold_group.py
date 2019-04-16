import sys
from functools import reduce

import cv2


class ThresholdGroup:
    def __init__(self, *thresholds, **kwargs):
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
        return reduce(lambda th_frame, threshold: self.binary_mask(th_frame, threshold(frame)), self.thresholds, 0)

    def __add__(self, other):
        return ThresholdGroup(self.thresholds + [other], binary_mask=self.binary_mask, default_pixel=self.default_pixel)

    def __iadd__(self, other):
        self.thresholds += [other]

    def __iter__(self):
        return iter(self.thresholds)

    def __len__(self):
        return len(self.thresholds)

    def __getitem__(self, item):
        return self.thresholds[item]

    def __setitem__(self, key, value):
        self.thresholds[key] = value
