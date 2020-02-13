import gbvision as gbv

THRESHOLD = gbv.ColorThreshold([[0, 62], [215, 255], [15, 95]], 'HSV')


def main():
    camera = gbv.AsyncUSBCamera(0)
    camera.wait_start_reading()
    window = gbv.CameraWindow('feed', camera)
    window.show_async()
    threshold_window = gbv.CameraWindow('threshold', camera, drawing_pipeline=THRESHOLD)
    threshold_window.show_async()
    denoising_window = gbv.CameraWindow('denoised', camera,
                                        drawing_pipeline=THRESHOLD + gbv.DistanceTransformThreshold(0.4))
    denoising_window.show()


if __name__ == '__main__':
    main()
