from gbvision.utils.net import AsyncStreamReceiver
from .udp_stream_receiver import UDPStreamReceiver


class AsyncUDPStreamReceiver(AsyncStreamReceiver, UDPStreamReceiver):

    def __init__(self, port, *args, **kwargs):
        UDPStreamReceiver.__init__(self, port, *args, **kwargs)
        AsyncStreamReceiver.__init__(self, *args, **kwargs)

    def _read(self):
        return UDPStreamReceiver.read(self)
