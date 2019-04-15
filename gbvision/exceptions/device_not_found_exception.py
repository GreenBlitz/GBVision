from .vision_exception import VisionException


class DeviceNotFoundException(VisionException):
    """
    this is raised when the program was not able to connect to the camera
    """
    pass
