import abc
from .camera import Camera
from gbvision.utils.async_readable import AsyncReadable


class AsyncCamera(Camera, AsyncReadable, abc.ABC):
    """
    an abstract class that represents an async camera
    the async camera is similar to a regular camera, but executes the read actions on another thread
    thus not blocking the processing thread

    you will usually want to inherit from this class and from another camera class in order to use the async functionality
    for example:

    Example::
        class AsyncUSBCamera(AsyncCamera, USBCamera):
            def _read(self) -> Tuple[bool, Frame]:
                return USBCamera.read(self)

            def __init__(self, port, data=UNKNOWN_CAMERA):
                USBCamera.__init__(self, port, data)
                AsyncCamera.__init__(self)
    """

    def __init__(self):
        AsyncReadable.__init__(self)
