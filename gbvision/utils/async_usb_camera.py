from .usb_camera import USBCamera
from .async_camera import AsyncCamera


AsyncUSBCamera = AsyncCamera.create_type(USBCamera)
