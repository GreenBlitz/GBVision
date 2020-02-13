from typing import List

import gbvision as gbv

K = 0.6

THRESHOLD = gbv.ColorThreshold([[0, 62], [215, 255], [15, 95]], 'HSV') + gbv.DistanceTransformThreshold(K)


def radius_restore() -> gbv.Number:
    return 1 + K


def circle_process(circs: List[gbv.Circle]) -> List[gbv.Circle]:
    return [(c[0], c[1] * radius_restore()) for c in circs]


def main():
    camera = gbv.AsyncUSBCamera(0)
    camera.wait_start_reading()
    window = gbv.CameraWindow('feed', camera,
                              drawing_pipeline=gbv.DrawCircles(THRESHOLD, (0, 255, 0), circle_process=circle_process))
    window.show_async()
    denoising_window = gbv.CameraWindow('denoised', camera,
                                        drawing_pipeline=THRESHOLD)
    denoising_window.show()


if __name__ == '__main__':
    main()
