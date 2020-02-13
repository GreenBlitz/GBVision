from gbvision.models.basic_ops import normalized_distance_transform
from gbvision.utils.thresholds.color_threshold import ColorThreshold
from gbvision.utils.pipeline import PipeLine
from gbvision.constants.types import Number


class DistanceTransformThreshold(PipeLine):
    """
    a pipeline factory that performs normalized distance transform and then a minimum threshold on the frame which
    removes from the original frame all white pixels that are at most min_distance_ratio normalized distance from the
    nearest black frame

    """
    def __init__(self, min_distance_ratio: Number):
        PipeLine.__init__(self)
        self.functions += (normalized_distance_transform + ColorThreshold([[min_distance_ratio, 1.0]],
                                                                          ColorThreshold.THRESH_TYPE_GRAY)).functions
