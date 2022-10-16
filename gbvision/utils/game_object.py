import cv2
import numpy as np

from gbvision.constants.math import EPSILON
import gbvision.utils.cameras as cameras
from gbvision.constants.types import Point, Contour, Number, Location


class GameObject:
    """
    constructor of the image object
    which is an object on field

    :param root_area: the square root of the surface area of the object in real life

    """

    def __init__(self, root_area: Number):
        self.root_area = root_area

    def distance(self, camera: cameras.Camera, root_area: Number) -> float:
        """
        Note: this measures the distance between the camera and the object, to use another measuring point
        calculate the norm of the location

        :param camera: the camera, can be either Camera or CameraList
        :param root_area: a float representing the square root of the area of the object
            (in pixels)
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return camera.get_data().focal_length * self.root_area / (root_area + EPSILON)

    def location(self, camera: cameras.Camera, root_area: Number, center: Point) -> Location:
        """
        Calculates the 3D location of this object, relative to the camera

        :param camera: the camera, can be either Camera or CameraList
        :param root_area: a float representing the square root of the area of the object (in pixels)
        :param center: the center (x,y) of this object in the frame
        :return: a 3d vector of the relative [x y z] location between the object and the camera/measuring point (in meters)
        """
        frame_center = camera.get_width(), camera.get_height()
        frame_center = np.array(frame_center) / 2
        x, y = np.array(center) - frame_center
        alpha = x * camera.get_data().fov_width / frame_center[0]
        beta = y * camera.get_data().fov_height / frame_center[1]
        rel = np.array([[np.sin(alpha), np.sin(beta),
                         np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]]) * self.distance(camera, root_area)
        return camera.get_data().rotation_matrix.dot(rel.T).flatten() + camera.get_data().offset
