from gbvision.constants.types import Number
from gbvision.constants.math import EPSILON


def almost_equal(x: Number, y: Number, delta: Number = EPSILON) -> bool:
    return -delta <= x - y <= delta
