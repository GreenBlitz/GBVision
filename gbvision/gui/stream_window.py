from threading import Thread

import cv2

from net import StreamReceiver
from utils import PipeLine


class StreamWindow:
    """
    a basic window that displays the stream from a stream receiver
    """

    def __init__(self, stream_receiver: StreamReceiver, drawing_pipeline=PipeLine(), exit_key='qQ',
                 window_name='stream'):
        """
        initializes the stream window
        :param stream_receiver: a stream receiver from which the stream receives it's frames
        :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
        :param exit_key: an array of keys (a string), when one of the keys are pressed the window will be closed
        :param window_name: the title of the window
        """
        self.stream_receiver = stream_receiver
        self.drawing_pipeline = drawing_pipeline
        self.exit_key = exit_key
        self.window_name = window_name

    def show(self, flags=cv2.WINDOW_FREERATIO):
        """
        display the stream video window
        :param flags: some opencv window flags
        """
        cv2.namedWindow(self.window_name, flags)
        while True:
            frame = self.stream_receiver.get_frame()
            if frame is not None:
                cv2.imshow(self.window_name, self.drawing_pipeline(frame))
            k = chr(cv2.waitKey(1) & 0xFF)
            if k in self.exit_key:
                cv2.destroyWindow(self.window_name)
                return

    def show_async(self, flags=cv2.WINDOW_FREERATIO):
        """
        opens the steam video window on another thread
        :param flags: some opencv window flags
        """
        Thread(target=self.show, args=(flags, )).start()
