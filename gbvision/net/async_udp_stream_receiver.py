from .udp_stream_receiver import UDPStreamReceiver
from threading import Thread

class AsyncUDPStreamReceiver(UDPStreamReceiver):
    """
    a udp streamer that reads from the socket on another thread
    recommended for use when multiple threads are reading from the streamer at the same time
    and also when the reading thread gets paused a lot
    for example when running a window that get's paused or moved around a lot
    """
    def __init__(self, port: int, fx: float = 1.0, fy: float = 1.0):
        UDPStreamReceiver.__init__(self, port, fx, fy)
        self._frame = None
        self._thread = Thread(target=self._receive_thread_function)
        self._thread.start()

    def _receive_thread_function(self):
        while True:
            self._frame = UDPStreamReceiver.get_frame(self)

    def get_frame(self):
        return self._frame