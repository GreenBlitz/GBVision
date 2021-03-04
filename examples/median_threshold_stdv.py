import cv2
import numpy as np

import gbvision as gbv

def max_error(frame):
    median = np.median(frame, axis=(0, 1)).astype(int)
    # print(median)
    errors = [[abs(median - cell) for cell in row] for row in frame]
    h, s, v = [], [], []
    for row in errors:
        for cell in row:
            h.append(cell[0])
            s.append(cell[1])
            v.append(cell[2])

    return [max(h), max(s), max(v)]


def main():
    camera = gbv.USBCamera(0)
    camera.set_exposure(-5)
    window = gbv.CameraWindow('feed', camera)
    window.open()
    while True:
        frame = window.show_and_get_frame()
        k = window.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('feed', frame)
            cutout = gbv.crop(frame, *bbox)
            stdv = max_error(cutout)

            #stdv = 2 * np.array([np.std([[row[i][j] for i in range(len(row))] for row in cutout]) for j in range(3)])
            # stdv[0] = 30
            # print(stdv)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    cv2.destroyAllWindows()

    print(thr)

    original = gbv.FeedWindow(window_name='original')
    after_proc = gbv.FeedWindow(window_name='after threshold', drawing_pipeline=thr)

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
