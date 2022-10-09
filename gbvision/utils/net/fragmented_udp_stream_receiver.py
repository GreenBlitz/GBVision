import struct
import time
from typing import Optional, Tuple

import typing

from .udp_stream_receiver import UDPStreamReceiver
from gbvision.constants.net import FRAGMENTED_UDP_HEADERS_STRUCT
from gbvision.constants.types import Number


class FragmentedUDPStreamReceiver(UDPStreamReceiver):
    """
    A UDP receiver that can de-fragment packets sent from the fragmented UDP broadcaster, and rebuild large
    frames from several chunks

    :param max_wait: the maximum time in seconds the receiver will wait for chunks of a frame to arrive from
    the moment it received the first chunk, if this time passed and not all fragments have arrived,
    the receiver will stop handling the current frame and move on the the next frame that will arrive
    can be None to not set a wait limit (same as infinity)
    If this value is too large, a single frame might block the entire receiver if not all fragments arrive
    If this value is too small, a frame might be dropped just because this time passed before all fragments
    could arrive
    """

    def __init__(self, *args, max_wait: Optional[Number] = 1, **kwargs):
        UDPStreamReceiver.__init__(self, *args, **kwargs)
        self.headers_size = struct.calcsize(FRAGMENTED_UDP_HEADERS_STRUCT)
        assert (max_wait is None) or (max_wait > 0), f"Invalid max wait value: {max_wait}"
        self.max_wait = max_wait

    def _read_single_fragment(self) -> Tuple[Tuple[int, int, int], bytes]:
        """
        Reads a single fragment from the UDP socket

        :return: A tuple of two values:
                 1. The fragment headers as a tuple of three values (frame_index, fragment_index, fragments_amount)
                 2. The fragment payload
        """
        fragment = UDPStreamReceiver._get_bytes(self)
        headers = fragment[:self.headers_size]
        fragment = fragment[self.headers_size:]
        return typing.cast(Tuple[int, int, int], struct.unpack(FRAGMENTED_UDP_HEADERS_STRUCT, headers)), fragment

    def _get_bytes(self) -> bytes:
        current_id = -1
        fragments = {}
        last_time = 0
        while True:
            (new_id, fragment_index, amount), fragment = self._read_single_fragment()
            if new_id > current_id:
                last_time = time.time()
                current_id = new_id
                fragments.clear()
            if new_id < current_id:
                continue
            fragments[fragment_index] = fragment
            if len(fragments) == amount:
                break
            if self.max_wait is not None and time.time() - last_time > self.max_wait:
                current_id = -1
        # we want the fragments in their correct order, not necessarily the order they arrived
        return b''.join([fragments[i] for i in range(len(fragments))])
