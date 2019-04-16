import gbvision as gbv


def main():
    camera = gbv.AsyncUSBCamera(1, gbv.LIFECAM_3000)
    orig_window = gbv.CameraWindow(camera, 'original')
    edges_window = gbv.CameraWindow(camera, 'edges', drawing_pipeline=gbv.edges + gbv.gray)
    orig_window.show_async()
    edges_window.show()


if __name__ == '__main__':
    main()
