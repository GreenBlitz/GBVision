import cv2
import numpy as np

from .camera import Camera
from models import contour_center


class GameObject:
    def __init__(self, area: float):
        """
        constructor of the image object
        which is an object on field
        :param area: the square root of the surface area of the object in real life
        """
        self.area = area

    def distance_by_pipeline(self, camera: Camera, pipeline, frame=None):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param pipeline: a pipeline that returns a float representing the square root of the area of the object
        (in pixels)
        :param frame: optional, a frame to be used instead of the next image from the camera
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return camera.data.focal_length * self.area / pipeline(camera.read()[1] if frame is None else frame)

    def location2d_by_pipeline(self, camera: Camera, pipeline, frame=None):
        """
        calculates the 2d location [x z] between the object and the camera
        :param camera: the camera, can be either Camera or CameraList
        :param pipeline: a pipeline that returns the contour of the object
        :param frame: optional, a frame to be used instead of the next image from the camera
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame = camera.read() if frame is None else frame
        cnt = pipeline(frame)
        return self.location2d_by_contours(camera, cnt)

    def distance_by_contours(self, camera: Camera, cnt):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return self.area * camera.focal_length / np.sqrt(cv2.contourArea(cnt))

    def location2d_by_contours(self, camera: Camera, cnt):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame_center = camera.width, camera.height
        frame_center = np.array(frame_center) / 2
        vp = contour_center(cnt)
        x, y = np.array(vp) - frame_center
        alpha = x * camera.fov / frame_center[0]
        return np.array([np.sin(alpha), np.cos(alpha)]) * self.distance_by_contours(camera, cnt)

    def distance_by_params(self, camera: Camera, area):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
        (in pixels)
        :return: the norm of the vector between the camera and the object (in meters)
        """
        return camera.focal_length * self.area / area

    def location2d_by_params(self, camera: Camera, area, center):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
        (in pixels)
        :param center: the center (x,y) of this object in the frame
        :return: a 2d vector of the relative [x z] location between the object and the camera (in meters)
        """
        frame_center = camera.width, camera.height
        frame_center = np.array(frame_center) / 2
        x, y = np.array(center) - frame_center
        alpha = x * camera.fov / frame_center[0]
        return np.array([np.sin(alpha), np.cos(alpha)]) * self.distance_by_params(camera, area)

    def location3d_by_pipeline(self, camera: Camera, pipeline, frame=None):
        """
        calculates the 2d location [x z] between the object and the camera
        :param camera: the camera, can be either Camera or CameraList
        :param pipeline: a pipeline that returns the contour of the object
        :param frame: optional, a frame to be used instead of the next image from the camera
        :return: a 3d vector of the relative [x y z] location between the object and the camera (in meters)
        """
        frame = camera.read() if frame is None else frame
        cnt = pipeline(frame)
        return self.location3d_by_contours(camera, cnt)

    def location3d_by_contours(self, camera: Camera, cnt):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param cnt: the contours of this object in the frame
        :return: a 3d vector of the relative [x y z] location between the object and the camera (in meters)
        """
        frame_center = camera.width, camera.height
        frame_center = np.array(frame_center) / 2
        vp = contour_center(cnt)
        x, y = np.array(vp) - frame_center
        alpha = x * camera.fov / frame_center[0]
        beta = y * camera.fov / frame_center[1]
        return np.array([np.sin(alpha), np.sin(beta),
                         np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]) * self.distance_by_contours(camera, cnt)

    def location3d_by_params(self, camera: Camera, area: float, center: (float or int, float or int)):
        """
        :param camera: the camera, can be either Camera or CameraList
        :param area: a float representing the square root of the area of the object
        (in pixels)
        :param center: the center (x,y) of this object in the frame
        :return: a 3d vector of the relative [x y z] location between the object and the camera (in meters)
        """
        frame_center = camera.width, camera.height
        frame_center = np.array(frame_center) / 2
        x, y = np.array(center) - frame_center
        alpha = x * camera.data.fov / frame_center[0]
        beta = y * camera.data.fov / frame_center[1]
        return np.array([np.sin(alpha), np.sin(beta),
                         np.sqrt(1 - np.sin(alpha) ** 2 - np.sin(beta) ** 2)]) * self.distance_by_params(camera, area)
