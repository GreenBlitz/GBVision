import cv2

from utils import PipeLine


class FeedWindow:
    def __init__(self, drawing_pipeline=PipeLine(), exit_button=('q', 'Q'),
                 window_name='feed'):
        self.drawing_pipeline = drawing_pipeline
        self.exit_button = exit_button
        self.window_name = window_name

    def start(self, flags=cv2.WINDOW_FREERATIO):
        cv2.namedWindow(self.window_name, flags)

    def show_frame(self, frame) -> bool:
        cv2.imshow(self.window_name, self.drawing_pipeline(frame))
        k = chr(cv2.waitKey(1) & 0xFF)
        if k == self.exit_button or k in self.exit_button:
            cv2.destroyWindow(self.window_name)
            return False
        return True

    def stop(self):
        cv2.destroyWindow(self.window_name)


