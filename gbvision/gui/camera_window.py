from .readable_window import ReadableWindow


class CameraWindow(ReadableWindow):
    """
    a basic window that displays a feed from a camera
    in this class, self.wrap_object will be of type Camera
    
    :type self.wrap_object: gbvision.Camera
    """
