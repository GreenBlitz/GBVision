import gbvision as gbv


def main():
    receiver = gbv.FragmentedUDPStreamReceiver(5808)
    window = gbv.StreamWindow(window_name='stream example', wrap_object=receiver)
    window.show()
    receiver.release()


if __name__ == '__main__':
    main()
