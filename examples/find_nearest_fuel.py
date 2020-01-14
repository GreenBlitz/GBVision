import gbvision as gbv

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.ColorThreshold([[0, 76], [215, 255], [40, 120]], 'HSV')


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL)
    while True:
        ok, frame = camera.read()
        all_fuels = find_fuel(frame, camera)
        if len(all_fuels) > 0:
            nearest_fuel = all_fuels[0]
            print('found fuel at distance %f meters and %f angles' % (
                gbv.distance_from_object(nearest_fuel),
                gbv.plane_angle_by_location(nearest_fuel)
            ))


if __name__ == '__main__':
    main()
