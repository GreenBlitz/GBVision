from gbvision.utils.thresholds.color_threshold import ColorThreshold
from gbvision.utils.pipeline import PipeLine


class DistanceTransformThreshold(PipeLine):
    """
    a pipeline factory that performs normalized distance transform and then a minimum threshold on the frame which
    removes from the original frame all white pixels that are at most min_distance_ratio normalized distance from the
    nearest black frame

    :param min_distance_ratio: the minimum ratio between the maximum distance of a pixel from a white pixel in the
        frame and a certain pixel for it to be included in the threshold, between 0 and 1
    """
    def __init__(self, min_distance_ratio: float):
        PipeLine.__init__(self)
        from gbvision.models.basic_ops import normalized_distance_transform
        self.functions += (normalized_distance_transform + ColorThreshold([[min_distance_ratio, 1.0]],
                                                                          ColorThreshold.THRESH_TYPE_GRAY)).functions
