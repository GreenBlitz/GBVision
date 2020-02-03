import abc

from gbvision.utils.net.stream_receiver import StreamReceiver
from gbvision.utils.async_readable import AsyncReadable


class AsyncStreamReceiver(AsyncReadable, StreamReceiver, abc.ABC):
    """
    an abstract async tcp stream receiver that receives frames on another thread
    None! when inheriting from this class and another StreamReceiver class, make sure you call the other class'
    constructor before this class' constructor, but also make sure you inherit from this class first in order
    """

    def __init__(self, *args, **kwargs):
        StreamReceiver.__init__(self, *args, **kwargs)
        AsyncReadable.__init__(self)
