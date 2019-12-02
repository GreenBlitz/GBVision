import gbvision as gbv

VISION_TARGET_THRESHOLD = gbv.ColorThreshold([[0, 25], [150, 255], [0, 25]], 'BGR')
# the vision target threshold, found using median threshold

VISION_TARGET = gbv.GameObject(0.08424226967)


# target size (in meters) is about 0.14x0.05
# the square root of this size is the constant above (0.0842422...)

def main():
    finder = gbv.TargetPairFinder(VISION_TARGET_THRESHOLD + gbv.Erode(3) + gbv.Dilate(4),
                                  VISION_TARGET)
    # define the target finder
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    # connect to camera
    camera.set_auto_exposure(False)
    # turn off auto exposure mode (on raspberry pi)
    camera.set_exposure(False)
    # turn exposure to minimum (on raspberry pi)
    while True:
        ok, frame = camera.read()
        if ok:
            hatches = finder(frame, camera)
            if len(hatches) > 0:
                closest_hatch = hatches[0]
                print('found hatch at distance: %s\nand angle: %s' % (
                    gbv.distance_from_object(closest_hatch), gbv.plane_angle_by_location(closest_hatch)))


if __name__ == '__main__':
    main()
