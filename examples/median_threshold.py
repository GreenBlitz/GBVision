import cv2
import numpy as np

import gbvision as gbv

stdv = np.array([40, 40, 40])


def main():
    camera = gbv.USBCamera(0, gbv.UNKNOWN_CAMERA)
    #camera.set_exposure(-1)
    cv2.namedWindow('window', cv2.WINDOW_FREERATIO)
    ok, frame = camera.read()
    while ok:
        ok, frame = camera.read()
        cv2.imshow('window', frame)

        k = chr(cv2.waitKey(1) & 0xFF)
        if k == 'r':
            bbox = cv2.selectROI('window', frame)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()

    print(thr)

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr + gbv.Erode(3) + gbv.Dilate(3))

    original.open()
    after_proc.open()
    while True:
        ok, frame = camera.read()
        if not original.show_frame(frame):
            break
        if not after_proc.show_frame(frame):
            break

    original.close()
    after_proc.close()


if __name__ == '__main__':
    main()
