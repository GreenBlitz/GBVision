from threading import Thread

import cv2

from net import StreamReceiver
from utils import PipeLine


class StreamWindow:
    def __init__(self, stream_receiver: StreamReceiver, drawing_pipeline=PipeLine(), exit_button=('q', 'Q'),
                 window_name='feed'):
        self.stream_receiver = stream_receiver
        self.drawing_pipeline = drawing_pipeline
        self.exit_button = exit_button
        self.window_name = window_name

    def show(self):
        cv2.namedWindow(self.window_name, cv2.WINDOW_FREERATIO)
        while True:
            frame = self.stream_receiver.get_frame()
            if frame is not None:
                cv2.imshow(self.window_name, self.drawing_pipeline(frame))
            k = cv2.waitKey(1)
            if k == self.exit_button or k in self.exit_button:
                cv2.destroyWindow(self.window_name)
                return

    def show_async(self):
        Thread(target=self.show).start()
