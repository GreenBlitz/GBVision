import gbvision as gbv

THRESHOLD_CONST = gbv.ColorThreshold([[0, 69], [181, 255], [85, 165]], 'HSV')
# found using median threshold

OBJECT_CONST = gbv.GameObject(0.04523893421169302263386206471922)


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    threshold_function = THRESHOLD_CONST + gbv.MedianBlur(5)
    finder = gbv.CircleFinder(threshold_function, OBJECT_CONST, contour_min_area=100)
    window = gbv.Window('feed')
    window.open()
    while window.is_opened():
        frame = window.show_and_get_frame()
        objects = finder(frame, camera)
        if len(objects):
            print("object is at distance: %s meters" % (gbv.distance_from_object(objects[0])))
    window.close()


if __name__ == '__main__':
    main()
