import socket

from gbvision.constants.net import LOCAL_SERVER_IP, UDP_MAX_SIZE
from .stream_receiver import StreamReceiver


class UDPStreamReceiver(StreamReceiver):
    """
    This class uses UDP to receive a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the client and the receiver is the server
    WARNING: Do not use this class to send large images, udp has a limited packet size
    To send a stream of frames larger then the maximum size of an IP packet, use FragmentedUDPStreamReceiver

    :param port: The UDP port to use
    """

    def __init__(self, port: int, *args, **kwargs):
        StreamReceiver.__init__(self, *args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (LOCAL_SERVER_IP, port)
        self.socket.bind(self.server_addr)

    def _get_bytes(self) -> bytes:
        return self.socket.recv(UDP_MAX_SIZE)

    def release(self) -> None:
        self.socket.close()

    def is_opened(self) -> bool:
        return self.socket.fileno() != -1
