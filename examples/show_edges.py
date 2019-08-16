import gbvision as gbv


def main():
    camera = gbv.AsyncUSBCamera(0, gbv.UNKNOWN_CAMERA)
    camera.set_frame_size(640, 480)
    orig_window = gbv.CameraWindow('original', camera)
    edges_window = gbv.CameraWindow('edges', camera, drawing_pipeline=gbv.edges + gbv.gray)
    orig_window.show_async()
    edges_window.show()


if __name__ == '__main__':
    main()
