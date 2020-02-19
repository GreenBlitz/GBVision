# constants
from .constants import *

# exceptions
from .exceptions import *

# gui
from .gui import *

# models
from .models import *

# tools
from .tools import *

# utils
from .utils import *


# configure opencv
def cv_config():
    """
    configure some opencv stuff so that it doesn't cause problems
    called automatically when importing gbvision, and does not need to be called by the user
    """
    import cv2
    if cv2.getVersionString()[0] == '2':
        for i in filter(lambda attr: attr.startswith("CV_CAP_PROP"), dir(cv2.cv)):
            object.__setattr__(cv2, i[3:], cv2.cv.__getattribute__(i))
            cv2.__dict__[i[3:]] = cv2.cv.__dict__[i]


cv_config()
del cv_config
