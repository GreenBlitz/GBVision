import pickle
import socket
import struct

import cv2

from gbvision.constants.net import LOCAL_SERVER_IP
from .stream_receiver import StreamReceiver


class UDPStreamReceiver(StreamReceiver):
    """
    this class uses UDP to receive a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the client and the receiver is the server
    WARNING: do not use this class to send large images, udp has a limited packet size
    """

    def __init__(self, port: int, shape=(0, 0), fx: float = 1.0, fy: float = 1.0):
        """

        :param port: the port which udp should use
        """
        StreamReceiver.__init__(self, shape=shape, fx=fx, fy=fy)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (LOCAL_SERVER_IP, port)
        self.socket.bind(self.server_addr)
        self.payload_size = struct.calcsize("I")
        self.data = b''

    def get_frame(self):
        self.data += self.socket.recv(2 ** 20)

        packed_msg_size = self.data[:self.payload_size]

        self.data = self.data[self.payload_size:]

        msg_size = struct.unpack("I", packed_msg_size)[0]

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)
        if frame is None:
            return None
        frame = cv2.imdecode(frame, -1)
        return cv2.resize(frame, (0, 0), fx=self.fx, fy=self.fy)
