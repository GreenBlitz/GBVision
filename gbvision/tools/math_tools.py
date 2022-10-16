from gbvision.constants.types import Number


def almost_equal(x: Number, y: Number, delta: Number = 0.001) -> bool:
    return -delta <= x - y <= delta
