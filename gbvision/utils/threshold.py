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
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def rgb_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def bgr_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def luv_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def lab_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def yuv_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


def xyz_threshold(frame, params):
    """
    thresholds the image according to RGB values
    :param frame: the image
    :param params: the hls values, 3x2 matrix of [hmin hmax]
                                                 [lmin lmax]
                                                 [smin smax]
    :return: binary threshold image
    """
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2XYZ)
    red, green, blue = params
    return cv2.inRange(frame, (red[0], green[0], blue[0]), (red[1], green[1], blue[1]))


THRESHOLD_NAME_TABLE = {
    'BGR': bgr_threshold,
    'RGB': rgb_threshold,
    'HLS': hls_threshold,
    'HSV': hsv_threshold,
    'LUV': luv_threshold,
    'LAB': lab_threshold,
    'YUV': yuv_threshold,
    'XYZ': xyz_threshold
}


class Threshold:
    def __init__(self, lst, thresh_type='HSV'):
        assert thresh_type.upper() in THRESHOLD_NAME_TABLE
        self.init = lst
        self.type = thresh_type.upper()

    def __len__(self):
        return len(self.init)

    def __getitem__(self, item):
        return self.init[item]

    def __setitem__(self, key, value):
        self.init[key] = value

    def __iter__(self):
        return iter(self.init)

    def __call__(self, frame):
        return THRESHOLD_NAME_TABLE[self.type](frame, self.init)

