import gbvision as gbv


def main():
    receiver = gbv.TCPStreamReceiver('127.0.0.1', 5808)
    window = gbv.RecordingStreamWindow(window_name='stream example', wrap_object=receiver, file_name='record.avi')
    window.show()


if __name__ == '__main__':
    main()
