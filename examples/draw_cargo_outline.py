import gbvision as gbv

CARGO_THRESHOLD = gbv.Threshold(  # cargo threshold constant, found using median threshold
    [[5, 15], [225, 255], [115, 175]],
    'HSV'
)


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    # connect to camera

    camera.set_auto_exposure(1)
    # switch to auto exposure mode
    # this works on windows, when using a raspberry pi use booleans instead

    threshold_func = gbv.EMPTY_PIPELINE + CARGO_THRESHOLD + gbv.Erode(3) + gbv.Dilate(3)
    # the full pipeline of thresholding and denoising

    window = gbv.CameraWindow(camera, 'camera 0',
                              drawing_pipeline=gbv.DrawCircles(  # draw the outline circles of the cargos
                                  threshold_func, (255, 0, 0),  # threshold and color is blue (bgr)
                                  contours_process=gbv.FilterContours(100),  # filter small contours
                                  circle_process=gbv.sort_circles + gbv.filter_inner_circles))  # sort circles and delete the inner circles

    window.show()


if __name__ == '__main__':
    main()
