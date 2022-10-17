import gbvision as gbv

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.ColorThreshold(((0, 76), (215, 255), (40, 120)), 'HSV')

TRACKER_TYPE = 'EMPTY'
SHAPE_TYPE = 'CIRCLE'

CONTOUR_MIN_AREA = 1000


def main():
    camera = gbv.USBCamera(0)
    camera.set_exposure(-2)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL, contours_hook=gbv.FilterContours(CONTOUR_MIN_AREA))
    window = gbv.CameraWindow('feed', camera,
                              drawing_pipeline=gbv.DrawCircles(find_fuel.find_shapes_unsorted, (0, 255, 0),
                                                               thickness=6))
    while True:
        ok, frame = window.read()
        fuels = find_fuel.find_shapes(frame)
        k = window.last_key_pressed
        if k == 'r':
            wrapper = gbv.ContinuesShapeWrapper(fuels, frame, find_fuel.find_shapes, shape_type=SHAPE_TYPE,
                                                tracker_type=TRACKER_TYPE, shape_lifespan=20, track_new=True)
            break
    window.release()
    window = gbv.FeedWindow('track')
    window.open()
    ok = True
    while ok:
        ok, frame = camera.read()
        fuels = wrapper.find_shapes(frame)

        for i, fuel in fuels.items():
            if fuel is None:
                continue
            frame = gbv.BaseCircle.draw(frame, fuel, (0, 255, 0), thickness=6)
            frame = gbv.draw_text(frame, f'ID: {i}', (int(fuel[0][0]) - 10, int(fuel[0][1]) - 10), 1, (0, 255, 0),
                                  thickness=3)
        if not window.show_frame(frame):
            break


if __name__ == '__main__':
    main()
