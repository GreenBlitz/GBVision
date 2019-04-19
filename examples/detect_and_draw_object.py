import gbvision as gbv

THRESHOLD_CONST = gbv.Threshold([[78, 98], [143, 203], [33, 133]], 'HSV')
# found using median threshold

OBJECT_CONST = gbv.GameObject(0.20706279240848655)

def main():
    camera = gbv.USBCamera(1, gbv.LIFECAM_3000)
    threshold_function = THRESHOLD_CONST + gbv.median_blur(5)
    finder = gbv.RotatedRectFinder(threshold_function, OBJECT_CONST, contour_min_area=100)
    window = gbv.FeedWindow(drawing_pipeline=gbv.draw_rotated_rects(
        threshold_func=threshold_function,
        color=(255, 0, 0),
        contours_process=gbv.filter_contours(1000),
        rotated_rects_process=gbv.sort_rotated_rects + gbv.filter_inner_rotated_rects
    ))
    window.open()
    frame = None
    while window.show_frame(frame):
        ok, frame = camera.read()
        objects = finder(frame, camera)
        if len(objects):
            print("object is at distance: %s meters" % (gbv.distance_from_object(objects[0])))


if __name__ == '__main__':
    main()
