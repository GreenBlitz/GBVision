import cv2

from utils import PipeLine


class FeedWindow:
    """
    a basic window class
    """
    def __init__(self, drawing_pipeline=PipeLine(), exit_key: str='qQ', window_name='feed'):
        """
        initializes the window
        :param drawing_pipeline: optional, a pre-processing pipeline that draws on the frame before displaying it
        :param exit_key: an array of chars (a string), which when pressed the window will stop displaying
        :param window_name: the title of the window
        """
        self.drawing_pipeline = drawing_pipeline
        self.exit_key = exit_key
        self.window_name = window_name

    def open(self, flags=cv2.WINDOW_FREERATIO):
        """
        initializes the window
        :param flags: some opencv window flags
        """
        cv2.namedWindow(self.window_name, flags)

    def show_frame(self, frame) -> bool:
        """
        shows the frame
        :param frame: the frame to show
        :return: True if the window is still open, False otherwise
        """
        cv2.imshow(self.window_name, self.drawing_pipeline(frame))
        k = chr(cv2.waitKey(1) & 0xFF)
        if k in self.exit_key:
            self.close()
            return False
        return True

    def close(self):
        """
        closes this window
        """
        cv2.destroyWindow(self.window_name)


