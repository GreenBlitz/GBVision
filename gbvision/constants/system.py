import cv2

from gbvision.utils.pipeline import PipeLine

CONTOURS_INDEX = 1 if cv2.getVersionString()[0] == '3' else 0

EMPTY_PIPELINE = PipeLine()
