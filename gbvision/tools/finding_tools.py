import numpy as np

distance_from_object = np.linalg.norm


def angle_by_location2d(loc):
    return np.arctan(loc[0] / loc[1])


def angle_by_location3d(loc):
    return np.arctan(loc[0] / loc[2])
