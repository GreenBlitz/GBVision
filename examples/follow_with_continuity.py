from gbvision.gui import drawing_functions

import gbvision as gbv
from gbvision.continuity.continues_circle import ContinuesCircle
from gbvision.gui.feed_window import FeedWindow

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.ColorThreshold([[0, 69], [181, 255], [85, 165]], 'HSV')


def main():
    camera = gbv.USBCamera(0, gbv.LIFECAM_3000)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL)
    ok, frame = camera.read()
    all_fuels = find_fuel.get_shapes(frame)
    nearest_fuel = None
    fuel_follower = None
    window = FeedWindow('bigganigga')
    if len(all_fuels) > 0:
        nearest_fuel = all_fuels[0]
        fuel_follower = ContinuesCircle(shape=nearest_fuel, frame=frame)
        found_fuel = True
    else:
        found_fuel = False
    while ok:
        ok, frame = camera.read()
        all_fuels = find_fuel.get_shapes(frame)
        if (not found_fuel) and len(all_fuels) > 0:
            nearest_fuel = all_fuels[0]
            fuel_follower = ContinuesCircle(shape=nearest_fuel, frame=frame)
            found_fuel = True
        if found_fuel:
            for check in all_fuels:
                if fuel_follower.update(frame=frame, shape=check):
                    nearest_fuel = check
                    break
        if len(all_fuels) == 0:
            found_fuel = False
        painted_frame = drawing_functions.draw_circles(frame= frame, circs= [nearest_fuel], color=(255,255,255))
        window.show_frame(painted_frame)


if __name__ == '__main__':
    main()
