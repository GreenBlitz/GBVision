import socket
import struct

from .stream_receiver import StreamReceiver
from gbvision.exceptions.tcp_stream_closed import TCPStreamClosed
from gbvision.constants.net import TCP_HEADERS_STRUCT


class TCPStreamReceiver(StreamReceiver):
    """
    this class uses TCP to receive a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the server and the receiver is the client

    :param ip: the IPv4 address of the stream broadcaster, for example '10.45.90.8'
    :param port: the port which TCP should use
    """

    def __init__(self, ip: str, port: int, *args, **kwargs):
        StreamReceiver.__init__(self, *args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (ip, port)
        self.socket.connect(self.server_addr)
        self.headers_size = struct.calcsize(TCP_HEADERS_STRUCT)

    def _receive(self):
        try:
            return self.socket.recv(2 ** 32)
        except OSError as e:
            raise TCPStreamClosed() from e

    def _get_bytes(self) -> bytes:
        data = b''
        while len(data) < self.headers_size:
            data += self._receive()
        packed_msg_size = data[:self.headers_size]
        data = data[self.headers_size:]
        msg_size = struct.unpack(TCP_HEADERS_STRUCT, packed_msg_size)[0]
        while len(data) < msg_size:
            data += self._receive()
        frame_data = data[:msg_size]
        return frame_data
