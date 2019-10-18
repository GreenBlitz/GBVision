import pickle
import socket
import struct

import cv2

from .stream_receiver import StreamReceiver
from gbvision.exceptions.tcp_stream_closed import TCPStreamClosed


class TCPStreamReceiver(StreamReceiver):
    """
    this class uses TCP to receive a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the server and the receiver is the client

    :param ip: the IPv4 address of the stream broadcaster, for example '10.45.90.8'
    :param port: the port which TCP should use
    """

    def __init__(self, ip: str, port: int, shape=(0, 0), fx: float = 1.0, fy: float = 1.0):
        """
        initializes the stream receiver
        
        """
        StreamReceiver.__init__(self, shape=shape, fx=fx, fy=fy)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.socket.connect(self.server_addr)
        self.payload_size = struct.calcsize("I")
        self.data = b''

    def get_frame(self):
        try:
            while len(self.data) < self.payload_size:
                self.data += self.socket.recv(4096)
        except OSError:
            raise TCPStreamClosed()

        packed_msg_size = self.data[:self.payload_size]

        self.data = self.data[self.payload_size:]

        msg_size = struct.unpack("I", packed_msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.socket.recv(4096)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)
        if frame is None:
            return None
        frame = cv2.imdecode(frame, -1)
        return self._prep_frame(frame)
