import gbvision as gbv

CARGO = gbv.GameObject(0.2926321307845007)

CARGO_THRESHOLD = gbv.Threshold(
    [[5, 15], [225, 255], [115, 175]],
    'HSV'
)


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
                gbv.angle_by_location3d(nearest_cargo)
            ))
