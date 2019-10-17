from gbvision.net.async_stream_receiver import AsyncStreamReceiver
from .udp_stream_receiver import UDPStreamReceiver


AsyncUDPStreamReceiver = AsyncStreamReceiver.create_type(UDPStreamReceiver)
