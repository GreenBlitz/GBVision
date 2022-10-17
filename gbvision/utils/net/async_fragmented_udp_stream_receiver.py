from .async_stream_receiver import AsyncStreamReceiver
from .fragmented_udp_stream_receiver import FragmentedUDPStreamReceiver


class AsyncFragmentedUDPStreamReceiver(AsyncStreamReceiver, FragmentedUDPStreamReceiver):
    def __init__(self, port, *args, **kwargs):
        FragmentedUDPStreamReceiver.__init__(self, port, *args, **kwargs)
        AsyncStreamReceiver.__init__(self, *args, **kwargs)

    def _read(self):
        return FragmentedUDPStreamReceiver.read(self)

    def _release(self) -> None:
        FragmentedUDPStreamReceiver.release(self)
