from .stream_broadcaster import StreamBroadcaster
from constants import LOCAL_SERVER_IP
import socket
import time
import pickle
import struct
import cv2


class TCPStreamBroadcaster(StreamBroadcaster):
    """
    this class uses TCP to send a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the server and the receiver is the client
    """
    def __init__(self, port: int, fx: float = 1.0, fy: float = 1.0, im_encode: str = '.jpg', use_grayscale: bool = False,
                 max_fps: int = None):
        """
        initializes the streamer
        :param port: the port which TCP will be using
        :param im_encode: the type of image encoding to send over the network, default is .jpg (JPEG)
        for missing parameters, see documentation on StreamBroadcaster
        """
        StreamBroadcaster.__init__(self, fx=fx, fy=fy, use_grayscale=use_grayscale, max_fps=max_fps)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (LOCAL_SERVER_IP, port)
        self.socket.bind(self.server_addr)
        self.socket.listen(10)
        self.socket, addr = self.socket.accept()
        self.payload_size = struct.calcsize("I")
        self.im_encode = im_encode
        self.prev_time = 0.0

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
        self.socket.send(data)  # to(data, self.server_addr)
        self.prev_time = time.time()
