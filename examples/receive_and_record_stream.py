import gbvision as gbv


def main():
    receiver = gbv.AsyncFragmentedUDPStreamReceiver(5808)
    receiver.wait_start_reading()
    window = gbv.RecordingStreamWindow(window_name='stream example', wrap_object=receiver, file_name='record.mp4')
    window.show()
    receiver.release()


if __name__ == '__main__':
    main()
