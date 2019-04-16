from threading import Thread

import cv2

from gbvision.utils.camera import Camera
from gbvision.utils.pipeline import PipeLine
from .window import Window


class CameraWindow(Window):
    """
    a basic window that displays a feed from a camera
    """

    def __init__(self, camera: Camera, window_name='stream', exit_button='qQ', drawing_pipeline=PipeLine()):
        """
        initializes the stream window
        :param camera: the camera to display the window from
        :param drawing_pipeline: optional, a pipeline of drawing functions that will run on the frame before displaying
        it
        :param exit_button: an array of keys (a string), when one of the keys are pressed the window will be closed
        :param window_name: the title of the window
        """
        Window.__init__(self, window_name, exit_button, drawing_pipeline)
        self.camera = camera

    def show(self, flags=cv2.WINDOW_FREERATIO):
        """
        display the camera video window
        :param flags: some opencv window flags
        """
        cv2.namedWindow(self.window_name, flags)
        while True:
            ok, frame = self.camera.read()
            if ok:
                cv2.imshow(self.window_name, self.drawing_pipeline(frame))
            k = chr(cv2.waitKey(1) & 0xFF)
            if k in self.exit_button:
                cv2.destroyWindow(self.window_name)
                return

    def show_async(self, flags=cv2.WINDOW_FREERATIO):
        """
        opens the camera video window on another thread
        :param flags: some opencv window flags
        """
        Thread(target=self.show, args=(flags,)).start()
