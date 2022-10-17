from typing import Union, Tuple

from .erode import Erode
from .dilate import Dilate

from gbvision.utils.pipeline import PipeLine


class ErodeAndDilate(PipeLine):
    """
    A pipeline class that erodes and dilates the given frame by the same kernel

    :param ksize: The kernel size, either an integer (meaning an nxn kernel) or a tuple (nxm kernel)
    :param iterations: Optional. The amount of Dilate iterations to perform, default is 1.
                       Note! a large number of iterations will slow down the program
    """

    def __init__(self, ksize: Union[int, Tuple[int, int]], iterations=1):
        PipeLine.__init__(self)
        self.functions += (Erode(ksize, iterations) + Dilate(ksize, iterations)).functions
