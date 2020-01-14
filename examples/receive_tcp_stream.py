import time

import gbvision as gbv


def main():
    receiver = gbv.AsyncTCPStreamReceiver('127.0.0.1', 5808)
    time.sleep(5)
    window = gbv.StreamWindow(window_name='stream example', wrap_object=receiver)
    window.show()


if __name__ == '__main__':
    main()
