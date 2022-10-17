from gbvision.constants.types import Number


def almost_equal(x: Number, y: Number, delta: Number = 0.001) -> bool:
    """
    Checks if two numbers are almost equal using the formula -delta <= x - y <= delta

    :param x: The first number
    :param y: The second number
    :param delta: The maximum allowed diff (default 0.001)
    :return: True if the numbers are almost equal, False otherwise
    """
    return -delta <= x - y <= delta
