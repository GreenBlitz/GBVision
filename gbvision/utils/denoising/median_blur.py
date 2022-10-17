import cv2

from gbvision.utils.pipeline import PipeLine


class MedianBlur(PipeLine):
    """
    Creates a pipeline that blurs the given frame using the median blur method
    Works very good for denoising purposes

    :param ksize: The size of the kernel used by the filter, must be an odd number
    :return: A pipeline that filters the image using the median blur method
    """

    def __init__(self, ksize: int):
        PipeLine.__init__(self, lambda frame: cv2.medianBlur(frame, ksize))
