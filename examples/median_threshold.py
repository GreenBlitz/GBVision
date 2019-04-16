import cv2
import numpy as np

import gbvision as gbv

stdv = np.array([20, 30, 30])


def threshold(frame, params):
    red, green, blue = params
    return cv2.inRange(frame, (int(red[0]), int(green[0]), int(blue[0])), (int(red[1]), int(green[1]), int(blue[1])))


def convert(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


def main():
    camera = gbv.USBCamera(0, gbv.GENERIC_CAMERA)

    while True:
        ok, frame = camera.read()
        cv2.imshow('window', frame)

        k = cv2.waitKey(1) & 0xFF
        if k == ord('r'):
            bbox = cv2.selectROI('window', frame)
            frame = convert(frame)
            ftag = gbv.crop(frame, *bbox)
            med = np.median(ftag, axis=(0, 1)).astype(int)

            params = np.vectorize(lambda x: min(255, max(0, x)))(np.array([med - stdv, med + stdv])).T
            break
        if k == ord('q'):
            break
    cv2.destroyAllWindows()
    print(list(map(list, params)))

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold',
                                drawing_pipeline=gbv.PipeLine(convert, lambda f: threshold(f, params)))

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
