import gbvision as gbv


def main():
    camera = gbv.USBCamera(0)
    window = gbv.RecordingCameraWindow(window_name='camera example', wrap_object=camera, file_name='record.avi')
    window.show()


if __name__ == '__main__':
    main()
