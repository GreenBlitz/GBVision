from .stream_camera import StreamCamera
from .usb_camera import USBCamera

USBStreamCamera = StreamCamera.create_type(USBCamera)
