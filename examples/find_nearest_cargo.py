import gbvision as gbv

CARGO = gbv.GameObject(0.04523893421169302263386206471922)

CARGO_THRESHOLD = gbv.ColorThreshold([[0, 76], [215, 255], [40, 120]], 'HSV')


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    find_cargo = gbv.CircleFinder(CARGO_THRESHOLD, CARGO)
    while True:
        ok, frame = camera.read()
        all_cargos = find_cargo(frame, camera)
        if len(all_cargos) > 0:
            nearest_cargo = all_cargos[0]
            print('found cargo at distance %f meters and %f angles' % (
                gbv.distance_from_object(nearest_cargo),
                gbv.plane_angle_by_location(nearest_cargo)
            ))


if __name__ == '__main__':
    main()
