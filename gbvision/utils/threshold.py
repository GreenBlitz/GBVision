import cv2


def hls_threshold(frame, params):
    """
    thresholds the image according to HLS values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def hsv_threshold(frame, params):
    """
    thresholds the image according to HSV values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [smin smax]
                                                 [vmin vmax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def rgb_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [rmin rmax]
                                                 [gmin gmax]
                                                 [bmin bmax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def bgr_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [bmin bmax]
                                                 [gmin gmax]
                                                 [rmin rmax]
    :return: binary threshold image
    """
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def luv_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [lmin lmax]
                                                 [umin umax]
                                                 [vmin vmax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def lab_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [lmin lmax]
                                                 [amin amax]
                                                 [bmin bmax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def yuv_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [ymin ymax]
                                                 [umin umax]
                                                 [vmin vmax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def xyz_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [xmin xmax]
                                                 [ymin ymax]
                                                 [zmin zmax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2XYZ)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def gray_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 1x2 matrix of [min max]
    :return: binary threshold image
    """
    if len(frame.shape) > 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.threshold(frame, params[0][0], params[0][1], cv2.THRESH_BINARY)[1]


THRESHOLD_NAME_TABLE = {
    'BGR': bgr_threshold,
    'RGB': rgb_threshold,
    'HLS': hls_threshold,
    'HSV': hsv_threshold,
    'LUV': luv_threshold,
    'LAB': lab_threshold,
    'YUV': yuv_threshold,
    'XYZ': xyz_threshold,
    'GRAY': gray_threshold
}


class Threshold:
    """
    a class that represents a function that maps from an image to a binary image
    where 255 states that the pixel at the original image was in a range represented by the threshold object
    and 0 states the pixel was out of the range
    for example:
    Threshold([[200, 255], [0, 50], [0, 50]], 'RGB')
    the above threshold represents a relatively red pixel. when an image is filtered by it, every pixel that is
    relatively red will be given the value 255, and every pixel that isn't will be given the value of 0
    """

    def __init__(self, pixel_range, thresh_type='HSV'):
        """
        initializes the threshold
        :param pixel_range: the threshold parameters, as a list of integers
        in the shape of 3x2 for a color image and 1x2 for a gray image
        :param thresh_type: a string, the type of color encoding to transform the image before applying the range test
        binary filter
        can be selected from the given list:
        'BGR': default opencv color encoding (no change)
        'RGB': default opencv color encoding in reverse
        'HLS': hue, luminous, saturation
        'HSV': hue, saturation, value
        'LUV': https://en.wikipedia.org/wiki/CIELUV
        'LAB': https://en.wikipedia.org/wiki/CIELAB_color_space
        'YUV': https://en.wikipedia.org/wiki/YUV
        'XYZ': https://en.wikipedia.org/wiki/CIE_1931_color_space
        'GRAY': grayscale images (single channel), image presented doesn't have to be gray, the threshold will convert
         it
        """
        assert thresh_type.upper() in THRESHOLD_NAME_TABLE
        self.params = pixel_range
        self.type = thresh_type.upper()

    def __len__(self):
        """
        the amount of parameters is equal to the amount of channels
        :return: 1 if the threshold is for grayscale images, 3 if it is for color images
        """
        return len(self.params)

    def __getitem__(self, item: int):
        """
        returns the item'th channel's range
        :param item: the index
        :return: the range of the pixel in the item'th channel
        """
        return self.params[item]

    def __setitem__(self, key: int, value: list or tuple):
        """
        sets the key'th channel's range to value
        :param key: the channel
        :param value: an array of 2 integers, the lower and upper bounds of the pixel
        """
        self.params[key] = value

    def __iter__(self):
        """
        :return: an iterator that iterates through the channel ranges
        """
        return iter(self.params)

    def __call__(self, frame):
        """
        activates the threshold filter on the given image
        :param frame: the image to activate the threshold on
        :return: a binary image, the frame after the threshold filter
        """
        return THRESHOLD_NAME_TABLE[self.type](frame, self.params)
