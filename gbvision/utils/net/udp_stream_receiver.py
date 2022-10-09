import socket

from gbvision.constants.net import LOCAL_SERVER_IP, UDP_MAX_SIZE
from .stream_receiver import StreamReceiver


class UDPStreamReceiver(StreamReceiver):
    """
    this class uses UDP to receive a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the client and the receiver is the server
    WARNING: do not use this class to send large images, udp has a limited packet size

    :param port: the port which udp should use
    """

    def __init__(self, port: int, *args, **kwargs):
        StreamReceiver.__init__(self, *args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (LOCAL_SERVER_IP, port)
        self.socket.bind(self.server_addr)

    def _get_bytes(self) -> bytes:
        return self.socket.recv(UDP_MAX_SIZE)
