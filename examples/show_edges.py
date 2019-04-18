import gbvision as gbv


def main():
    camera = gbv.AsyncUSBCamera(0, gbv.UNKNOWN_CAMERA)
    orig_window = gbv.CameraWindow(camera, 'original')
    edges_window = gbv.CameraWindow(camera, 'edges', drawing_pipeline=gbv.edges + gbv.gray)
    orig_window.show_async()
    edges_window.show()


if __name__ == '__main__':
    main()
