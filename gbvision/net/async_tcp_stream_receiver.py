from .tcp_stream_receiver import TCPStreamReceiver
from threading import Thread


class AsyncTCPStreamReceiver(TCPStreamReceiver):
    """
    a tcp streamer that reads from the socket on another thread
    recommended for use when multiple threads are reading from the streamer at the same time
    and also when the reading thread gets paused a lot
    for example when running a window that get's paused or moved around a lot
    """

    def __init__(self, ip: str, port: int, shape=(0, 0), fx=1.0, fy=1.0):
        TCPStreamReceiver.__init__(self, ip=ip, port=port, shape=shape, fx=fx, fy=fy)
        self._frame = None
        self._thread = Thread(target=self._receive_thread_function)
        self._thread.start()

    def _receive_thread_function(self):
        while True:
            self._frame = TCPStreamReceiver.get_frame(self)

    def get_frame(self):
        return self._frame
