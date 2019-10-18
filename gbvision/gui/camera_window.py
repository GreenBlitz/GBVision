from .wrapper_opencv_window import WrapperOpenCVWindow


class CameraWindow(WrapperOpenCVWindow):
    """
    a basic window that displays a feed from a camera
    in this class, self.wrap_object will be of type Camera
    :type self.wrap_object: gbvision.Camera
    """
    def _get_frame(self):
        _, frame = self.wrap_object.read()
        return frame
