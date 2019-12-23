import gbvision as gbv

FUEL = gbv.GameObject(0.04523893421169302263386206471922)

FUEL_THRESHOLD = gbv.ColorThreshold([[0, 73], [129, 209], [119, 199]], 'HSV')


def main():
    camera = gbv.USBCamera(0)
    find_fuel = gbv.CircleFinder(FUEL_THRESHOLD, FUEL, contour_min_area=1000)
    fuel_follower = None
    window = gbv.FeedWindow('follow')
    window.open()
    ok = True
    found_fuel = False
    tracker = gbv.Tracker('MEDIANFLOW')
    while ok:
        ok, frame = camera.read()
        all_fuels = find_fuel.find_shapes(frame)
        if (not found_fuel) and len(all_fuels) > 0:
            nearest_fuel = all_fuels[0]
            fuel_follower = gbv.ContinuesCircle(shape=nearest_fuel, frame=frame, tracker=tracker)
            found_fuel = True
        if found_fuel:
            for check in all_fuels:
                if fuel_follower.update(frame=frame, shape=check):
                    break
            else:
                fuel_follower.update_forced(frame=frame)
            frame = gbv.draw_circles(frame=frame, circs=[fuel_follower.get()],
                                     color=(255, 0, 0), thickness=10)

        if len(all_fuels) == 0:
            found_fuel = False
        if fuel_follower is not None and fuel_follower.is_lost(max_count=20):
            found_fuel = False
        if not window.show_frame(frame):
            break


if __name__ == '__main__':
    main()
