from typing import List, Tuple, Union

import cv2

from gbvision.utils.thresholds.threshold import Threshold
from gbvision.constants.types import Number, Frame, ColorThresholdParams, GrayScaleThresholdParams


def bgr_threshold(frame: Frame, params: ColorThresholdParams):
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


class __ColorThresholdFunction:
    def __init__(self, color_type: int):
        self.color_type = color_type

    def __call__(self, frame: Frame, params: ColorThresholdParams):
        frame = cv2.cvtColor(frame, self.color_type)
        return bgr_threshold(frame, params)


hls_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2HLS)
hsv_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2HSV)
rgb_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2RGB)
luv_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2LUV)
lab_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2LAB)
yuv_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2YUV)
xyz_threshold = __ColorThresholdFunction(cv2.COLOR_BGR2XYZ)


def gray_threshold(frame: Frame, params: GrayScaleThresholdParams):
    if len(frame.shape) > 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(frame, params[0], params[0], cv2.THRESH_BINARY)[1]


class ColorThreshold(Threshold):
    """
    a class that represents a function that maps from an image to a binary image
    where 255 states that the pixel at the original image was in a range represented by the threshold object
    and 0 states the pixel was out of the range
    for example:
    Threshold([[200, 255], [0, 50], [0, 50]], 'RGB')
    the above threshold represents a relatively red pixel. when an image is filtered by it, every pixel that is
    relatively red will be given the value 255, and every pixel that isn't will be given the value of 0


    :param pixel_range: the threshold parameters, as a list of integers
        in the shape of 3x2 for a color image and 1x2 for a gray image
    :param thresh_type: a string, the type of color encoding to transform the image before applying the range test \
        binary filter \
        can be selected from the given list: \
        'BGR': default opencv color encoding (no change) \
        'RGB': default opencv color encoding in reverse \
        'HLS': hue, luminous, saturation \
        'HSV': hue, saturation, value \
        'LUV': https://en.wikipedia.org/wiki/CIELUV \
        'LAB': https://en.wikipedia.org/wiki/CIELAB_color_space \
        'YUV': https://en.wikipedia.org/wiki/YUV \
        'XYZ': https://en.wikipedia.org/wiki/CIE_1931_color_space \
        'GRAY': grayscale images (single channel), image presented doesn't have to be gray, the threshold will convert it
    """

    THRESH_TYPE_BGR = 'BGR'
    THRESH_TYPE_RGB = 'RGB'
    THRESH_TYPE_HLS = 'HLS'
    THRESH_TYPE_HSV = 'HSV'
    THRESH_TYPE_LUV = 'LUV'
    THRESH_TYPE_LAB = 'LAB'
    THRESH_TYPE_YUV = 'YUV'
    THRESH_TYPE_XYZ = 'XYZ'
    THRESH_TYPE_GRAY = 'GRAY'

    _THRESHOLD_NAME_TABLE = {
        THRESH_TYPE_BGR: bgr_threshold,
        THRESH_TYPE_RGB: rgb_threshold,
        THRESH_TYPE_HLS: hls_threshold,
        THRESH_TYPE_HSV: hsv_threshold,
        THRESH_TYPE_LUV: luv_threshold,
        THRESH_TYPE_LAB: lab_threshold,
        THRESH_TYPE_YUV: yuv_threshold,
        THRESH_TYPE_XYZ: xyz_threshold,
        THRESH_TYPE_GRAY: gray_threshold
    }

    def __init__(self, pixel_range: Union[ColorThresholdParams, GrayScaleThresholdParams], thresh_type=THRESH_TYPE_BGR):
        assert thresh_type.upper() in self._THRESHOLD_NAME_TABLE
        self.params = pixel_range
        self.type = thresh_type.upper()

    def __len__(self):
        """
        The amount of parameters is equal to the amount of channels

        :return: 1 if the threshold is for grayscale images, 3 if it is for color images
        """
        return len(self.params)

    def __getitem__(self, item: int):
        """
        Returns the item'th channel's range

        :param item: the index
        :return: the range of the pixel in the item'th channel
        """
        return self.params[item]

    def __iter__(self):
        """
        :return: An iterator that iterates through the channel ranges
        """
        return iter(self.params)

    def _threshold(self, frame):
        """
        Activates the threshold filter on the given image

        :param frame: the image to activate the threshold on
        :return: a binary image, the frame after the threshold filter
        """
        return self._THRESHOLD_NAME_TABLE[self.type](frame, self.params)

    def __repr__(self):
        return f'<{self}>'

    def __str__(self):
        return f"ColorThreshold({self.params}, '{self.type}')"
