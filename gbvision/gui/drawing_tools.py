from gbvision.constants.types import Color, FilterFunction

from gbvision.models.system import EMPTY_PIPELINE
from gbvision.models.contours import find_contours, contours_to_circles, contours_to_rects, contours_to_rotated_rects, \
    contours_to_ellipses
from gbvision.utils.pipeline import PipeLine
from .drawing_functions import draw_contours, draw_circles, draw_rects, draw_rotated_rects, draw_ellipses


class _DrawObject(PipeLine):
    def __init__(self, finding_func, color, drawing_func, *args, **kwargs):
        def _draw(frame):
            return drawing_func(frame, finding_func(frame), color, *args, **kwargs)

        PipeLine.__init__(self, _draw)


class DrawContours(_DrawObject):
    """
    a pipeline that draws all contours according to the given parameters, and returns a copy of the frame after drawing
    """

    def __init__(self, threshold_func: FilterFunction, color: Color, contours_process=EMPTY_PIPELINE, *args,
                 **kwargs):
        contour_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process
        _DrawObject.__init__(self, contour_finding, color, draw_contours, *args, **kwargs)


class DrawCircles(_DrawObject):
    """
    a pipeline that draws all circles according to the given parameters, and returns a copy of the frame after drawing
    """

    def __init__(self, threshold_func: FilterFunction, color: Color, contours_process=EMPTY_PIPELINE,
                 circle_process=EMPTY_PIPELINE, *args, **kwargs):
        circle_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_circles + \
                         circle_process

        _DrawObject.__init__(self, circle_finding, color, draw_circles, *args, **kwargs)


class DrawRects(_DrawObject):
    """
    a pipeline that draws all rects according to the given parameters, and returns a copy of the frame after drawing
    """

    def __init__(self, threshold_func: FilterFunction, color: Color, contours_process=EMPTY_PIPELINE,
                 rects_process=EMPTY_PIPELINE, *args, **kwargs):
        rect_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_rects + \
                       rects_process

        _DrawObject.__init__(self, rect_finding, color, draw_rects, *args, **kwargs)


class DrawRotatedRects(_DrawObject):
    """
    a pipeline that draws all rotated rects according to the given parameters, and returns a copy of the frame after drawing
    """

    def __init__(self, threshold_func: FilterFunction, color: Color, contours_process=EMPTY_PIPELINE,
                 rotated_rects_process=EMPTY_PIPELINE, *args, **kwargs):
        rotated_rect_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_rotated_rects + \
                               rotated_rects_process

        _DrawObject.__init__(self, rotated_rect_finding, color, draw_rotated_rects, *args, **kwargs)


class DrawEllipses(_DrawObject):
    """
    a pipeline that draws all ellipses according to the given parameters, and returns a copy of the frame after drawing
    """

    def __init__(self, threshold_func: FilterFunction, color: Color, contours_process=EMPTY_PIPELINE,
                 ellipses_process=EMPTY_PIPELINE, *args, **kwargs):
        ellipses_finding = EMPTY_PIPELINE + threshold_func + find_contours + contours_process + contours_to_ellipses + \
                           ellipses_process

        _DrawObject.__init__(self, ellipses_finding, color, draw_ellipses, *args, **kwargs)
