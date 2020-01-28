from .camera import Camera
import freenect
import numpy as np


class KinectCamera(Camera):
    def __init__(self, port):
        self.port = port

    @staticmethod
    def pretty_depth(depth):
        """
        Converts depth into a 'nicer' format for display

        :param depth: A numpy array with 2 bytes per pixel
        
        :return: A numpy array that has been processed with unspecified datatype
        """
        np.clip(depth, 0, 2**10-1, depth)
        depth >>=2
        depth=depth.astype(np.uint8)
        return depth
    
    @staticmethod
    def get_ir_video(self):
        frame = freenect.sync_get_video(self.port, freenect.VIDEO_IR_10BIT)[0]
        frame = pretty_depth(frame)
        return frame
    
    @staticmethod
    def get_depth_image(self):
        frame = freenect.sync_get_video(self.port)[0]
        frame = pretty_depth(frame)
        return frame
    


