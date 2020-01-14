import gbvision as gbv


def main():
    broadcaster = gbv.UDPStreamBroadcaster('127.0.0.1', 5808)
    camera = gbv.USBStreamCamera(broadcaster, 0)
    camera.toggle_stream(True)
    while True:
        camera.read()


if __name__ == '__main__':
    main()
