import socket
import struct

from gbvision.constants.net import LOCAL_SERVER_IP, TCP_HEADERS_STRUCT
from gbvision.exceptions.tcp_stream_closed import TCPStreamClosed
from .stream_broadcaster import StreamBroadcaster


class TCPStreamBroadcaster(StreamBroadcaster):
    """
    This class uses TCP to send a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the server and the receiver is the client
    
    :param port: The TCP port to use
    """

    def __init__(self, port: int, *args, **kwargs):
        StreamBroadcaster.__init__(self, *args, **kwargs)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_addr = (LOCAL_SERVER_IP, port)
        self.socket.bind(self.server_addr)
        self.socket.listen(10)
        self.socket, addr = self.socket.accept()

    def _send_bytes(self, data):
        try:
            data = struct.pack(TCP_HEADERS_STRUCT, len(data)) + data
            self.socket.send(data)
        except IOError as e:
            raise TCPStreamClosed() from e
        self._update_time()

    def release(self) -> None:
        self.socket.close()

    def is_opened(self) -> bool:
        return self.socket.fileno() != -1
