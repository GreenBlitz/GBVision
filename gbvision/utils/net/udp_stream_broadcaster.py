import socket
from .stream_broadcaster import StreamBroadcaster


class UDPStreamBroadcaster(StreamBroadcaster):
    """
    this class uses UDP to send a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the client and the receiver is the server
    WARNING: do not use this class to send large images, udp has a limited packet size

    :param ip: the IPv4 address of the udp stream receiver, for example '10.45.90.5'
    :param port: the port that UDP uses to send packets on
    :param im_encode: the type of image encoding to send over the network, default is '.jpg' (JPEG)
    """

    def __init__(self, ip: str, port: int, *args, **kwargs):
        StreamBroadcaster.__init__(self, *args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (ip, port)

    def _send_frame(self, frame):
        self.socket.sendto(frame, self.server_addr)
