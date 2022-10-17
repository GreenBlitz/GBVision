import cv2

from gbvision.constants.types import Frame, Color, Coordinates, Number


def draw_text(frame: Frame, text: str, coords: Coordinates, font_scale: Number, color: Color,
              font=cv2.FONT_HERSHEY_SIMPLEX, *args, **kwargs) -> Frame:
    """
    Draws the text on a copy of the frame and returns the copy

    :param frame: The frame to draw on
    :param text: The text to draw
    :param coords: The coordinates of the bottom-left corner of the text
    :param font_scale: The size of the drawn text (multiplied by the default size of the font)
    :param color: The color to draw the text in
    :param font: The font, an opencv font constant, default is cv2.FONT_HERSHEY_SIMPLEX
    :param args: Additional arguments to cv2.putText
    :param kwargs: Additional keyword arguments to cv2.putText (such as thickness)
    :return: A copy of the frame with the text drawn on it
    """
    frame = frame.copy()
    cv2.putText(frame, text, coords, font, font_scale, color, *args, **kwargs)
    return frame
