import cv2

CONTOURS_INDEX = 1 if cv2.getVersionString()[0] == '3' else 0


def cv_config():
    if cv2.__version__[0] == '2':
        for i in [attr for attr in dir(cv2.cv) if attr.startswith("CV_CAP_PROP")]:
            object.__setattr__(cv2, i[3:], cv2.cv.__getattribute__(i))
            cv2.__dict__[i[3:]] = cv2.cv.__dict__[i]

