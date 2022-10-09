import socket
import struct

from gbvision.constants.net import LOCAL_SERVER_IP, TCP_HEADERS_STRUCT
from .stream_broadcaster import StreamBroadcaster
from gbvision.exceptions.tcp_stream_closed import TCPStreamClosed


class TCPStreamBroadcaster(StreamBroadcaster):
    """
    this class uses TCP to send a stream over the network, the stream is by default set to be MJPEG
    the broadcaster is the server and the receiver is the client
    
    :param port: the port which TCP will be using
    :param im_encode: the type of image encoding to send over the network, default is .jpg (JPEG)
        for missing parameters, see documentation on StreamBroadcaster
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
