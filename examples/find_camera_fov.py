import numpy as np
import cv2
import gbvision as gbv


# angle = np.arctan(Wm / D / Wp * Wf)

def main():
    print('place object in the middle of the frame and press r')
    width = ord(input('Enter object width in meters >>> '))
    height = ord(input('Enter object height in meters >>> '))
    z = ord(input('Enter distance from object in the Z axis in meter units >>> '))
    camera = gbv.USBCamera(0)
    camera.set_exposure(-5)
    window = gbv.CameraWindow('feed', camera)
    window.open()
    while True:
        frame = window.show_and_get_frame()
        k = window.last_key_pressed
        if k == 'r':
            bbox = cv2.selectROI('feed', frame)
            fov = find_fov(bbox, width, height, z, (camera.get_width(), camera.get_height))
            break
    cv2.destroyAllWindows()

    print(f'width fov: {fov[0]}\nheight fov:{fov[1]}')

def find_fov(bbox: gbv.ROI, width: gbv.Number, height: gbv.Number, z: gbv.Number, camera_dimension):
    return np.arctan((width * bbox[0]) / (z * camera_dimension[0])), np.arctan((height * bbox[1]) / (z * camera_dimension[1]))


if __name__ == '__main__':
    main()
