import socket
from .stream_broadcaster import StreamBroadcaster
from gbvision.constants.net import UDP_MAX_SIZE


class UDPStreamBroadcaster(StreamBroadcaster):
    """
    this class uses UDP to send a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the client and the receiver is the server
    WARNING: Do not use this class to send large images, UDP has a limited packet size (the IPv4 limit)
    To send a stream of frames larger then the maximum size of an IP packet, use FragmentedUDPStreamBroadcaster

    :param ip: The IPv4 address of the udp stream receiver, for example '10.45.90.5'
    :param port: The UDP port to use
    """

    def __init__(self, ip: str, port: int, *args, **kwargs):
        StreamBroadcaster.__init__(self, *args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (ip, port)

    @staticmethod
    def _is_frame_legal_size(data: bytes) -> bool:
        """
        Checks if the data's size is too large for a single UDP packet

        :param data: The data to try and send
        :return: True if the data is small enough, False otherwise
        """
        return len(data) < UDP_MAX_SIZE

    def _can_send_bytes(self, data: bytes) -> bool:
        return self._is_frame_legal_size(data) and StreamBroadcaster._can_send_bytes(self, data)

    def _send_bytes(self, data: bytes) -> None:
        self.socket.sendto(data, self.server_addr)

    def release(self) -> None:
        self.socket.close()

    def is_opened(self) -> bool:
        return self.socket.fileno() != -1
