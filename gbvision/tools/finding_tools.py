import numpy as np

from gbvision.constants.types import Location


def distance_from_object(loc: Location) -> float:
    """
    the absolute distance from the camera to this object

    :param loc: the object's location (2d or 3d)
    :returns: the absolute distance (float)
    """
    if len(loc) <= 3:
        return np.linalg.norm(loc)
    return np.linalg.norm(loc[:3])


def plane_angle_by_location(loc: Location) -> float:
    """
    calculates the angle from the camera to the object's projection on the x-z plane (y=0 plane)

    :param loc: the 3d location
    :return: the angle (in radians)
    """
    return np.arctan(loc[0] / loc[2])


def plane_distance_from_object(loc: Location) -> float:
    """
    calculates the distance from the object's projection on the x-z plane (y=0 plane)
    the distance on the y axis is ignored in this calculation
    
    :param loc: the 3d location
    :return: the distance without regarding the y axis
    """
    return np.sqrt(loc[0] ** 2 + loc[2] ** 2)


def viewing_angle_of_object(part1: Location, part2: Location, x_distance: float) -> float:
    """
    finds the viewing angle of an object based on a split of the object to two parts (part1 and part2), and the x \
    distance between those two parts in real life (in meters)

    :param part1: the first part of the object (the left one)
    :param part2: the second part of the object (the right one)
    :param x_distance: the distance between the two objects in meters

    :return: the viewing angle of the object
    """
    return np.pi / 2 - np.arccos(max(-1, min(1, (part1[2] - part2[2]) / x_distance)))
