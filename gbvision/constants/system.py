import cv2

from gbvision.utils.pipeline import PipeLine

CONTOURS_INDEX = 1 if cv2.getVersionString()[0] == '3' else 0

EMPTY_PIPELINE = PipeLine()


def cv_config():
    """
    configure some opencv stuff so that it doesn't cause problems
    called automatically when importing gbvision, and does not need to be called by the user
    """
    if cv2.__version__[0] == '2':
        for i in [attr for attr in dir(cv2.cv) if attr.startswith("CV_CAP_PROP")]:
            object.__setattr__(cv2, i[3:], cv2.cv.__getattribute__(i))
            cv2.__dict__[i[3:]] = cv2.cv.__dict__[i]
