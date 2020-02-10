import cv2
import numpy as np

from gbvision.constants.math import EPSILON
import gbvision.utils.cameras as cameras
from gbvision.models.contours import contour_center
from gbvision.constants.types import Point, Contour, Number, Location


class GameObject:
    """
    constructor of the image object
    which is an object on field

    :param area: the square root of the surface area of the object in real life

    """

    def __init__(self, area: Number):
        self.area = area

    def distance_by_contours(self, camera: cameras.Camera, cnt: Contour) -> float:
        """
        Note: this measures the distance between the camera and the object, to use another measuring point
        calculate the norm of the location
        
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return self.distance_by_params(camera, np.sqrt(cv2.contourArea(cnt)))

    def distance_by_params(self, camera: cameras.Camera, area: Number) -> float:
        """
        Note: this measures the distance between the camera and the object, to use another measuring point
        calculate the norm of the location

        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
            (in pixels)
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return camera.get_data().focal_length * self.area / (area + EPSILON)

    def location_by_contours(self, camera: cameras.Camera, cnt: Contour) -> Location:
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: a 3d vector of the relative [x y z] location between the object and the camera (in meters)
        """
        return self.location_by_params(camera, np.sqrt(cv2.contourArea(cnt)), contour_center(cnt))

    def location_by_params(self, camera: cameras.Camera, area: Number, center: Point) -> Location:
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object (in pixels)
        :param center: the center (x,y) of this object in the frame
        :return: a 3d vector of the relative [x y z] location between the object and the camera/measuring point (in meters)
        """
        frame_center = camera.get_width(), camera.get_height()
        frame_center = np.array(frame_center) / 2
        x, y = np.array(center) - frame_center
        alpha = x * camera.get_data().fov_width / frame_center[0]
        beta = y * camera.get_data().fov_height / frame_center[1]
        rel = np.array([[np.sin(alpha), np.sin(beta),
                         np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]]) * self.distance_by_params(camera, area)
        return camera.get_data().rotation_matrix.dot(rel.T).flatten() + camera.get_data().offset
