import gbvision as gbv


def main():
    broadcaster = gbv.TCPStreamBroadcaster(5808)
    camera = gbv.USBStreamingCamera(broadcaster, 0)
    camera.toggle_stream(True)
    while True:
        try:
            camera.read()
        except gbv.TCPStreamClosed:
            broadcaster.release()


if __name__ == '__main__':
    main()
