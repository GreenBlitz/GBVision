import numpy as np

import gbvision as gbv

stdv = np.array([10, 80, 80])


def main():
    camera = gbv.USBCamera(0)
    camera.set_exposure(-5)
    window = gbv.CameraWindow('feed', camera)
    window.open()
    while True:
        ok, frame = window.read()
        k = window.last_key_pressed
        if k == 'r':
            bbox = window.select_roi(frame)
            thr = gbv.median_threshold(frame, stdv, bbox, 'HSV')
            break
    window.release()

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

    original.release()
    after_proc.release()


if __name__ == '__main__':
    main()
