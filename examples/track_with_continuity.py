import gbvision as gbv
import cv2

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.ColorThreshold([[0, 76], [215, 255], [40, 120]], 'HSV')

TRACKER_TYPE = 'EMPTY'
SHAPE_TYPE = 'CIRCLE'


def main():
    camera = gbv.USBCamera(0)
    camera.set_exposure(-5)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL, contour_min_area=1000)
    wrapper = None
    ok = True
    while ok:
        ok, frame = camera.read()
        fuels = find_fuel.find_shapes(frame)
        cv2.imshow('window', gbv.draw_circles(frame, list(fuels), (0, 255, 0), thickness=6))
        k = chr(cv2.waitKey(1) & 0xFF)
        if k == 'r':
            wrapper = gbv.ContinuesShapeWrapper(fuels, frame, find_fuel.find_shapes, shape_type=SHAPE_TYPE,
                                                tracker_type=TRACKER_TYPE, shape_lifespam=20, track_new=True)
            break
    cv2.destroyAllWindows()
    window = gbv.FeedWindow('track')
    window.open()
    ok = True
    while ok:
        ok, frame = camera.read()
        fuels = wrapper.find_shapes(frame)

        for i, fuel in fuels.items():
            if fuel is None:
                continue
            frame = gbv.draw_circles(frame, [fuel], (0, 255, 0), thickness=6)
            frame = gbv.draw_text(frame, str(f'ID: {i}'), (int(fuel[0][0]) - 10, int(fuel[0][1]) - 10), 1, (0, 255, 0),
                                  thickness=3)
        if not window.show_frame(frame):
            break


if __name__ == '__main__':
    main()
