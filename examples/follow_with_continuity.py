import gbvision as gbv
from gbvision.continuity.continues_circle import ContinuesCircle

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.Threshold([[80, 160], [18, 98], [6, 86]], 'HSV')


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL)
    ok, frame = camera.read()
    all_fuels = find_fuel.get_shape(frame)
    nearest_fuel = None
    fuel_follower = None
    if len(all_fuels) > 0:
        nearest_fuel = all_fuels[0]
        fuel_follower = ContinuesCircle(shape=nearest_fuel, frame=frame)
    found_fuel = False
    while True:
        ok, frame = camera.read()
        all_fuels = find_fuel.get_shape(frame)
        if (not found_fuel) and len(all_fuels) > 0:
            nearest_fuel = all_fuels[0]
            fuel_follower = ContinuesCircle(shape=nearest_fuel, frame=frame)
            found_fuel = True
        if found_fuel:
            fuel_follower.update(frame=frame, shape=nearest_fuel)
            if len(all_fuels) > 0:
                print(fuel_follower.get())


if __name__ == '__main__':
    main()
