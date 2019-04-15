from .vision_exception import VisionException


class CouldNotReadFrameException(VisionException):
    """
    this is raised when the camera could not be read from
    """
    pass
