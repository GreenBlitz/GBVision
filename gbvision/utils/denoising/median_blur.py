import cv2

from gbvision.utils.pipeline import PipeLine


class MedianBlur(PipeLine):
    """
    creates a pipeline that blurs the given frame using the median blur method
    works very good for denoising purposes

    :param ksize: the size of the kernel used by the filter, must be an odd number
    :return: a pipeline that filters the image using the median blur method
    """

    def __init__(self, ksize: int):
        PipeLine.__init__(self, lambda frame: cv2.medianBlur(frame, ksize))
