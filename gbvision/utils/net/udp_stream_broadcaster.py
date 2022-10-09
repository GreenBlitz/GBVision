import socket
from .stream_broadcaster import StreamBroadcaster
from gbvision.constants.net import UDP_MAX_SIZE


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

    @staticmethod
    def _is_frame_legal_size(frame: bytes) -> bool:
        """
        Checks if the frame's size is too large

        :param frame:
        :return:
        """
        return len(frame) < UDP_MAX_SIZE

    def _can_send_bytes(self, data: bytes) -> bool:
        return self._is_frame_legal_size(data) and StreamBroadcaster._can_send_bytes(self, data)

    def _send_bytes(self, data: bytes) -> None:
        self.socket.sendto(data, self.server_addr)
