from gbvision.net.async_stream_receiver import AsyncStreamReceiver
from .tcp_stream_receiver import TCPStreamReceiver


class AsyncTCPStreamReceiver(AsyncStreamReceiver, TCPStreamReceiver):

    def __init__(self, ip, port, shape=(0, 0), fx=1.0, fy=1.0):
        TCPStreamReceiver.__init__(self, ip, port, shape, fx, fy)
        AsyncStreamReceiver.__init__(self, shape, fx, fy)

    def _get_frame(self):
        return TCPStreamReceiver.get_frame(self)
