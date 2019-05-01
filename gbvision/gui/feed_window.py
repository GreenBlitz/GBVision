import cv2

from gbvision.constants.system import EMPTY_PIPELINE


class FeedWindow:
    """
    a basic window class
    """
    def __init__(self, window_name='feed', exit_button: str='qQ', drawing_pipeline=EMPTY_PIPELINE):
        """
        initializes the window
        :param drawing_pipeline: optional, a pre-processing pipeline that draws on the frame before displaying it
        :param exit_button: an array of chars (a string), which when pressed the window will stop displaying
        :param window_name: the title of the window
        """
        self.drawing_pipeline = drawing_pipeline
        self.exit_button = exit_button
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
        if frame is not None:
            cv2.imshow(self.window_name, self.drawing_pipeline(frame))
            k = chr(cv2.waitKey(1) & 0xFF)
            if k in self.exit_button:
                self.close()
                return False
        return True

    def close(self):
        """
        closes this window
        """
        cv2.destroyWindow(self.window_name)


