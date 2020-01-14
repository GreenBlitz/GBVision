import gbvision as gbv
import time


def main():
    camera = gbv.AsyncUSBCamera(0)
    camera.wait_start_reading()
    camera.set_frame_size(640, 480)
    orig_window = gbv.CameraWindow('original', camera)
    edges_window = gbv.CameraWindow('edges', camera, drawing_pipeline=gbv.edges + gbv.gray)
    orig_window.show_async()
    edges_window.show()


if __name__ == '__main__':
    main()
