import gbvision as gbv


def main():
    camera = gbv.USBCamera(0)
    window = gbv.RecordingCameraWindow(window_name='camera example', wrap_object=camera, file_name='record.avi',
                                       fps=camera.get_fps())
    window.show()
    camera.release()


if __name__ == '__main__':
    main()
