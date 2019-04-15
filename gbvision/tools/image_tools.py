def crop(frame, x, y, w, h):
    """
    crops the image from (x, y) to (x+w, y+h)
    :param frame: the frame to crop
    :param x: the x coordinate to crop from
    :param y: the y coordinate to crop from
    :param w: the width of the cropped image
    :param h: the height of the cropped image
    :return: the cropped image
    """
    return frame[y:y + h, x:x + w, :]
