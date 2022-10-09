import struct
from math import ceil

from .udp_stream_broadcaster import UDPStreamBroadcaster
from gbvision.constants.net import UDP_MAX_SIZE, FRAGMENTED_UDP_HEADERS_STRUCT
from gbvision.constants.types import Number, Frame


class FragmentedUDPStreamBroadcaster(UDPStreamBroadcaster):
    """
    A UDP broadcaster that can fragment big frames and send them in chunks, thus allowing it to bypass the
    size limit of the UDP broadcaster

    :param mtu: the maximum size of a single fragment (without the fragment headers)
    """

    HEADER_SIZE = struct.calcsize(FRAGMENTED_UDP_HEADERS_STRUCT)

    def __init__(self, *args, mtu: Number = UDP_MAX_SIZE - HEADER_SIZE, **kwargs):
        UDPStreamBroadcaster.__init__(self, *args, **kwargs)
        assert self.HEADER_SIZE < mtu <= (UDP_MAX_SIZE - self.HEADER_SIZE), f"Invalid MTU value: {mtu}"
        self.mtu = mtu
        self.current_index = 0

    @staticmethod
    def _is_frame_legal_size(frame: bytes) -> bool:
        return True

    def _send_single_fragment(self, fragment: bytes, index: int, amount: int) -> None:
        """
        Sends the given fragment with the correct headers

        :param fragment: The fragment
        :param index: The fragment's index in the entire frame
        :param amount: The total amount of fragments that will be sent
        """
        assert len(fragment) <= self.mtu, f"Cannot send fragment of size {len(fragment)} when MTU is {self.mtu}"
        UDPStreamBroadcaster._send_bytes(self,
                                         struct.pack(FRAGMENTED_UDP_HEADERS_STRUCT, self.current_index, index,
                                                     amount) + fragment)

    def _send_bytes(self, data: Frame) -> None:
        fragments_needed = int(ceil(len(data) / self.mtu))
        for i in range(fragments_needed):
            self._send_single_fragment(data[i * self.mtu:min((i + 1) * self.mtu, len(data))], i, fragments_needed)
        self.current_index = (self.current_index + 1) & 0xffffffff
