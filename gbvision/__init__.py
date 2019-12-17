# cameras
from .cameras.camera import Camera
from .cameras.stream_camera import StreamCamera
from .cameras.camera_data import CameraData
from .cameras.usb_camera import USBCamera
from .cameras.camera_list import CameraList
from .cameras.usb_stream_camera import USBStreamCamera
from .cameras.async_camera import AsyncCamera
from .cameras.async_usb_camera import AsyncUSBCamera

# constants
from .constants.cameras import LIFECAM_3000, LIFECAM_STUDIO, UNKNOWN_CAMERA
from .constants.math import EPSILON, SQRT_PI
from .constants.system import EMPTY_PIPELINE
from .constants.types import RotatedRect, Frame, Color, Circle, Contour, Rect, FixedPolygon, Ellipse, Polygon, Point

# continuity
from .continuity.continues_circle import ContinuesCircle
from .continuity.continues_rect import ContinuesRect
from .continuity.continues_rotated_rect import ContinuesRotatedRect
from .continuity.continues_shape import ContinuesShape
from .continuity.continues_shape_wrapper import ContinuesShapeWrapper

# exceptions
from .exceptions.vision_warning import VisionWarning
from .exceptions.vision_exception import VisionException
from .exceptions.could_not_read_frame_exception import CouldNotReadFrameException
from .exceptions.device_not_found_exception import DeviceNotFoundException
from .exceptions.stream_closed import StreamClosed
from .exceptions.tcp_stream_closed import TCPStreamClosed

# finders
from .finders.object_finder import ObjectFinder
from .finders.circle_finder import CircleFinder
from .finders.rect_finder import RectFinder
from .finders.polygon_finder import PolygonFinder
from .finders.rotated_rect_finder import RotatedRectFinder
from .finders.target_pair_finder import TargetPairFinder

# gui
from .gui.window import Window
from .gui.stream_window import StreamWindow
from .gui.feed_window import FeedWindow
from .gui.camera_window import CameraWindow
from .gui.recording_camera_window import RecordingCameraWindow
from .gui.recording_stream_window import RecordingStreamWindow
from .gui.drawing_tools import DrawCircles, DrawContours, DrawEllipses, DrawRects, DrawRotatedRects
from .gui.recording_feed_window import RecordingFeedWindow
from .gui.drawing_functions import draw_ellipses, draw_rotated_rects, draw_rects, draw_circles, draw_contours, draw_text
from .gui.recording_wrapper_opencv_window import RecordingWrapperOpenCVWindow
from .gui.recording_opencv_window import RecordingOpenCVWindow
from .gui.recording_window import RecordingWindow
from .gui.wrapper_opencv_window import WrapperOpenCVWindow
from .gui.wrapper_window import WrapperWindow
from .gui.opencv_window import OpenCVWindow

# models
from .models.basic_ops import corners, edges, sharpen, blur, blue, red, green, gray
from .models.contours import contour_center, contours_centers, contours_to_circles, contours_to_circles_sorted, \
    contours_to_ellipses, contours_to_ellipses_sorted, contours_to_polygons, contours_to_rects, \
    contours_to_rects_sorted, contours_to_rotated_rects, contours_to_rotated_rects_sorted, FilterContours, \
    find_contours, sort_contours, sort_rects, sort_circles, sort_rotated_rects, sort_ellipses
from .models.shapes import circle_collision, filter_inner_circles, filter_inner_rects, rect_collision, \
    rotated_rect_collision, convex_shape_collision, filter_inner_convex_shapes, filter_inner_rotated_rects
from .models.denoising import Dilate, MedianBlur, Erode

# net
from .net.stream_receiver import StreamReceiver
from .net.stream_broadcaster import StreamBroadcaster
from .net.tcp_stream_broadcaster import TCPStreamBroadcaster
from .net.tcp_stream_receiver import TCPStreamReceiver
from .net.udp_stream_broadcaster import UDPStreamBroadcaster
from .net.udp_stream_receiver import UDPStreamReceiver
from .net.async_tcp_stream_receiver import AsyncTCPStreamReceiver
from .net.async_udp_stream_receiver import AsyncUDPStreamReceiver

# thresholds
from .thresholds.color_threshold import ColorThreshold
from .thresholds.threshold import Threshold, ThresholdGroup

# tools
from .tools.list_tools import split_list
from .tools.image_tools import crop, median_threshold
from .tools.finding_tools import distance_from_object, plane_angle_by_location, plane_distance_from_object

# utils
from .utils.pipeline import PipeLine
from .utils.game_object import GameObject
from .utils.tracker import Tracker


# configure opencv
def cv_config():
    """
    configure some opencv stuff so that it doesn't cause problems
    called automatically when importing gbvision, and does not need to be called by the user
    """
    import cv2
    if cv2.__version__[0] == '2':
        for i in filter(lambda attr: attr.startswith("CV_CAP_PROP"), dir(cv2.cv)):
            object.__setattr__(cv2, i[3:], cv2.cv.__getattribute__(i))
            cv2.__dict__[i[3:]] = cv2.cv.__dict__[i]


cv_config()
del cv_config
