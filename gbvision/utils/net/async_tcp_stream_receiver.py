from gbvision.utils.net import AsyncStreamReceiver
from .tcp_stream_receiver import TCPStreamReceiver


class AsyncTCPStreamReceiver(AsyncStreamReceiver, TCPStreamReceiver):

    def __init__(self, ip, port, *args, **kwargs):
        TCPStreamReceiver.__init__(self, ip, port, *args, **kwargs)
        AsyncStreamReceiver.__init__(self, *args, **kwargs)

    def _read(self):
        return TCPStreamReceiver.read(self)
