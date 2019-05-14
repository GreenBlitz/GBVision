import gbvision as gbv

THRESHOLD_CONST = gbv.Threshold([[0, 98], [0, 203], [0, 133]], 'HSV')
# found using median threshold

OBJECT_CONST = gbv.GameObject(0.20706279240848655)


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    threshold_function = THRESHOLD_CONST + gbv.MedianBlur(5)
    finder = gbv.RotatedRectFinder(threshold_function, OBJECT_CONST, contour_min_area=100)
    window = gbv.FeedWindow('feed', drawing_pipeline=gbv.DrawRotatedRects(
        threshold_func=threshold_function,
        color=(255, 0, 0),
        contours_process=gbv.FilterContours(1000),
        rotated_rects_process=gbv.sort_rotated_rects + gbv.filter_inner_rotated_rects
    ))
    window.open()
    frame = None
    while window.show_frame(frame):
        ok, frame = camera.read()
        objects = finder(frame, camera)
        if len(objects):
            print("object is at distance: %s meters" % (gbv.distance_from_object(objects[0])))
    window.close()


if __name__ == '__main__':
    main()
