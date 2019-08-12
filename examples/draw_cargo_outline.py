import gbvision as gbv

CARGO_THRESHOLD = gbv.Threshold(  # cargo threshold constant, found using median threshold
    [[0, 28], [210, 250], [235, 255]],
    # [[14, 54], [1, 41], [233, 255]],
    'HSV'
)


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    camera.resize(0.75, 0.75)
    # connect to camera

    camera.set_exposure(-4)
    # switch to auto exposure mode
    # this works on windows, when using a raspberry pi use booleans instead

    threshold_func = gbv.EMPTY_PIPELINE + CARGO_THRESHOLD + gbv.Erode(5) + gbv.Dilate(10)
    # the full pipeline of thresholding and denoising

    window = gbv.CameraWindow('camera 0', camera,
                              drawing_pipeline=gbv.DrawCircles(  # draw the outline circles of the cargos
                                  threshold_func, (255, 0, 0),  # threshold and color is blue (bgr)
                                  contours_process=gbv.FilterContours(100),  # filter small contours
                                  circle_process=gbv.sort_circles + gbv.filter_inner_circles))  # sort circles and delete the inner circles

    window.show()


if __name__ == '__main__':
    main()
