import gbvision as gbv


def main():
    broadcaster = gbv.TCPStreamBroadcaster(5808)
    camera = gbv.USBStreamCamera(broadcaster, 0, gbv.LIFECAM_3000)
    camera.toggle_stream(True)
    while True:
        camera.read()


if __name__ == '__main__':
    main()
