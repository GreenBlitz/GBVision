from gbvision.net.async_stream_receiver import AsyncStreamReceiver
from .udp_stream_receiver import UDPStreamReceiver


class AsyncUDPStreamReceiver(AsyncStreamReceiver, UDPStreamReceiver):

    def __init__(self, port, shape=(0, 0), fx=1.0, fy=1.0):
        UDPStreamReceiver.__init__(self, port, shape, fx, fy)
        AsyncStreamReceiver.__init__(self, shape, fx, fy)

    def _get_frame(self):
        return UDPStreamReceiver.get_frame(self)
