import cv2

CONTOURS_INDEX = 1 if cv2.getVersionString()[0] == '3' else 0
