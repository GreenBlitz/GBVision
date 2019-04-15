import gbvision as gbv


def main():
    receiver = gbv.TCPStreamReceiver('127.0.0.1', 5808)
    window = gbv.StreamWindow(receiver, window_name='stream example')
    window.show()


if __name__ == '__main__':
    main()
