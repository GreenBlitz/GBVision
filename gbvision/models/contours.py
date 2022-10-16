from typing import List

import cv2

from gbvision.constants.system import CONTOURS_INDEX
from gbvision.constants.types import Contour, Polygon, Frame
from gbvision.utils.pipeline import PipeLine


@PipeLine
def find_contours(frame: Frame) -> List[Contour]:
    """
    Finds the contours in a binary frame

    :param frame: The frame (usually after threshold and denoising)
    :return: A list of all the contours in the frame
    """
    # DO NOT CHANGE THE CHAIN_APPROX_NONE
    # You do not know the damages it may cause
    return cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[CONTOURS_INDEX]


class FilterContours(PipeLine):
    """
    A pipeline factory that receives a list of contours and filters out all contours with an area less then defined
    to the pipeline

    :param min_area: the minimal area of a contour in order for it to pass the filter
    """

    def __init__(self, min_area: float):
        PipeLine.__init__(self, lambda cnts: filter(lambda c: cv2.contourArea(c) >= min_area, cnts), list)


convex_hull = PipeLine(cv2.convexHull)

convex_hull_multiple = PipeLine(lambda x: list(map(convex_hull, x)))


# SHAPES

@PipeLine
def fix_contours_shape(cnts: List[Contour]) -> List[Polygon]:
    """
    fixes the contours to a usable shape
    the shape of the contours is a list of tuples of integers/floats, where each tuple is a point
    an example of two rectangles represented with this shape will be:
    [[(0, 0), (0, 2), (1, 2), (1, 0)],
    [(5, 4), (7, 4), (7, 9), (9, 5)]]
    
    :param cnts: the contours / polygons list whose shape should be fixed
    :return: a list of all the contours with the fixed shape
    """
    cnts = map(lambda polydp: map(lambda x: x[0], polydp), cnts)
    return list(map(lambda polydp: list(map(tuple, polydp)), cnts))
