import pickle
import socket
import struct
import time

import cv2

from .stream_broadcaster import StreamBroadcaster


class UDPStreamBroadcaster(StreamBroadcaster):
    """
    this class uses UDP to send a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the client and the receiver is the server
    WARNING: do not use this class to send large images, udp has a limited packet size
    """

    def __init__(self, ip: str, port: int, shape=(0, 0), fx: float = 1.0, fy: float = 1.0, im_encode: str = '.jpg',
                 use_grayscale: bool = False, max_fps: int = None):
        """
        initializes a new udp stream broadcaster
        :param ip: the IPv4 address of the udp stream receiver, for example '10.45.90.5'
        :param port: the port that UDP uses to send packets on
        :param im_encode: the type of image encoding to send over the network, default is '.jpg' (JPEG)
        """
        StreamBroadcaster.__init__(self, shape=shape, fx=fx, fy=fy, use_grayscale=use_grayscale, max_fps=max_fps)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.payload_size = struct.calcsize("I")
        self.im_encode = im_encode
        self.prev_time = 0

    def send_frame(self, frame):
        if self.max_fps is not None and (time.time() - self.prev_time) * self.max_fps < 1:
            return
        if frame is not None:
            frame = cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
            if self.use_grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.imencode(self.im_encode, frame)[1]
        data = pickle.dumps(frame)
        data = struct.pack("I", len(data)) + data
        self.socket.sendto(data, self.server_addr)  # to(data, self.server_addr)
        self.prev_time = time.time()
