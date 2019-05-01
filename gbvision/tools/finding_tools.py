import numpy as np


def distance_from_object(loc) -> float:
    """
    the absolute distance from the camera to this object
    :param loc: the object's location (2d or 3d)
    :returns: the absolute distance (float)
    """
    if len(loc) <= 3:
        return np.linalg.norm(loc)
    return np.linalg.norm(loc[:3])


def angle_by_location(loc) -> float:
    """
    calculates the angle from the camera to the object
    :param loc: the 3d location
    :return: the angle (in radians)
    """
    return np.arctan(loc[0] / loc[2])

def plane_distance_from_object(loc) -> float:
    """
    calculates the distance from the object on the x-z plane
    the distance on the y axis is ignored in this calculation
    :param loc: the 3d location
    :return: the distance without regarding the y axis
    """
    return np.sqrt(loc[0]**2 + loc[2]**2)