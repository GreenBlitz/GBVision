import gbvision as gbv
import time


def main():
    camera = gbv.USBCamera(0)
    camera.set_frame_size(640, 480)
    orig_window = gbv.FeedWindow('original')
    edges_window = gbv.FeedWindow('edges', drawing_pipeline=gbv.edges)
    while True:
        ok, frame = camera.read()
        if not orig_window.show_frame(frame) or not edges_window.show_frame(frame):
            break
    orig_window.close()
    edges_window.close()


if __name__ == '__main__':
    main()
