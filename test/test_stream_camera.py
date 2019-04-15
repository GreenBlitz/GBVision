import gbvision as gbv
import cv2


def main():
    camera = gbv.USBStreamCamera(gbv.UDPStreamBroadcaster(ip='127.0.0.1', port=1337), 0, None)

    while 1:
        ok, frame = camera.read()
        cv2.imshow('feed', frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()
