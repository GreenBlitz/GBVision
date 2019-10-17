import gbvision as gbv
import time


def main():
    receiver = gbv.AsyncTCPStreamReceiver('127.0.0.1', 5808)
    time.sleep(5)  # wait for stream to connect
    window = gbv.RecordingStreamWindow(window_name='stream example', wrap_object=receiver, file_name='record.avi')
    window.show()


if __name__ == '__main__':
    main()
