import struct
from math import ceil

from .udp_stream_broadcaster import UDPStreamBroadcaster
from gbvision.constants.net import UDP_MAX_SIZE, FRAGMENTED_UDP_HEADERS_STRUCT
from gbvision.constants.types import Number


class FragmentedUDPStreamBroadcaster(UDPStreamBroadcaster):
    """
    a UDP broadcaster that can fragment big frames and send them in chunks, thus allowing it to bypass the
    size limit of the UDP broadcaster

    :param mtu: the maximum size of a single fragment (without the fragment headers)
    """

    def __init__(self, *args, mtu: Number = 60000, **kwargs):
        UDPStreamBroadcaster.__init__(self, *args, **kwargs)
        self.headers_size = struct.calcsize(FRAGMENTED_UDP_HEADERS_STRUCT)
        assert self.headers_size < mtu < (UDP_MAX_SIZE - self.headers_size)
        self.mtu = mtu
        self.current_index = 0xfffffffe

    @staticmethod
    def _is_frame_legal_size(frame: bytes) -> bool:
        return True

    def _send_single_fragment(self, fragment, index, amount):
        UDPStreamBroadcaster._send_bytes(self,
                                         struct.pack(FRAGMENTED_UDP_HEADERS_STRUCT, self.current_index, index,
                                                     amount) + fragment)

    def _send_bytes(self, frame):
        fragments_needed = int(ceil(len(frame) / self.mtu))
        for i in range(fragments_needed):
            self._send_single_fragment(frame[i * self.mtu:min((i + 1) * self.mtu, len(frame))], i, fragments_needed)
        self.current_index = (self.current_index + 1) & 0xffffffff
