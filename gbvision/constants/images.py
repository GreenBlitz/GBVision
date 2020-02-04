import cv2

COLOR_TYPE = {
    name[10:]: getattr(cv2, name) for name in dir(cv2) if name.startswith('COLOR_BGR2')
}
