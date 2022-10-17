import cv2

from .base_rotated_rect import BaseRotatedRect
from gbvision.constants.types import Ellipse, Frame, Color


class BaseEllipse(BaseRotatedRect):

    @staticmethod
    def _unsafe_draw(frame: Frame, shape: Ellipse, color: Color, *args, **kwargs) -> None:
        cv2.ellipse(frame, shape, color, *args, **kwargs)

    @staticmethod
    def collision(shape1: Ellipse, shape2: Ellipse) -> bool:
        return NotImplemented

    from_contour = cv2.fitEllipse
