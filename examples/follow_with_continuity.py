import gbvision as gbv
from gbvision.continuity.continues_circle import ContinuesCircle

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.Threshold([[0, 72], [126, 206], [140, 220]], 'HSV')


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL)
    ok, frame = camera.read()
    all_fuels = find_fuel.get_circles(frame)
    print(all_fuels)
    nearest_fuel = None
    fuel_follower = None
    if len(all_fuels) > 0:
        nearest_fuel = all_fuels[0]
        print(nearest_fuel[1])
        fuel_follower = ContinuesCircle(shape=nearest_fuel, frame=frame)
    found_fuel = False
    while True:
        frame = camera.read()
        all_fuels = find_fuel.get_circles(frame)
        if nearest_fuel is None and len(all_fuels) > 0:
            nearest_fuel = all_fuels[0]
            fuel_follower = ContinuesCircle(shape=nearest_fuel, frame=frame)
            found_fuel = True
        if found_fuel:
            fuel_follower.update()
        print(fuel_follower.get())

if __name__ == '__main__':
    main()
