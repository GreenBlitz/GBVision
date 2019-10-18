import numpy as np
from copy import deepcopy


class CameraData:
    """
    describes constant about a camera in it's default state used to approximate distance
    between the camera and an object seen in a frame
    """

    def __init__(self, focal_length, fov, yaw_angle=0, pitch_angle=0, roll_angle=0, x_offset=0, y_offset=0, z_offset=0, constant=False):
        """

        :param focal_length: the focal length of the camera at it's default state, in units of pixels
        can be described as the square root of the amount of pixels an object takes on a frame, multiplied by it's
        distance from the camera and divided by the square root of it's surface
        FOCAL_LENGTH = sqrt(P) * D / sqrt(W*H)
        where P is the amount of pixels in the frame representing the object,
        D is the real life distance between the object and the camera
        W is the real life width of the object
        H is the real life height of the object
        note that this is a constant, whatever object you choose to use, this formula will yield the same result
        :param fov:
        half the viewing angle of the camera (field of view) in radians, can be calculated by placing an object in front
        of the camera, so that the entire object is captured and it's center is at the frame's center.
        the tangent of the angle can be described as the width of the object in real life, divided by the
        product of the object's distance from the camera in real life and the ratio between the width of the frame
        in pixels and the width of the object in the frame, also in pixels
        tan(FOV) = (Wm) / (D * (Wp/Wf))
        where Wm is the real life width of the object
        D is the real life distance between the object and the camera
        Wp is the width of the object in the frame (pixels unit)
        Wf is the width of the frame (pixels unit)
        to calculate the FOV just apply the inverse tangent
        FOV = arctan(tan(FOV))
        :param yaw_angle:
        the clockwise yaw angle (in radians) in which the camera is rotated, the yaw angle is the angle around the y axis,
        it's output only affects the x and z axises.
        set this variable when the camera is rotated around the y axis and you want the output of finder functions
        to represent the original space, rather then the rotated one.
        :param pitch_angle:
        the clockwise pitch angle (in radians) in which the camera is rotated, the pitch angle is the angle around the x axis,
        it's output only affects the y and z axises.
        set this variable when the camera is rotated around the x axis and you want the output of finder functions
        to represent the original space, rather then the rotated one.
        :param roll_angle:
        the clockwise roll angle (in radians) in which the camera is rotated, the roll angle is the angle around the z axis,
        it's output only affects the x and y axises.
        set this variable when the camera is rotated around the z axis and you want the output of finder functions
        to represent the original space, rather then the rotated one.
        :param x_offset:
        the x offset in which the camera is placed
        the distance from the measuring point (usually the center of the robot) to the camera on the x axis (left/right),
        if the camera is to the right this should be positive and if it is left this should be negative
        :param y_offset:
        the y offset in which the camera is placed
        the distance from the measuring point to the camera on the y axis (up/down), if the camera is above the measuring point
        this variable should be positive and if it is below this should be negative
        :param z_offset:
        the z offset in which the camera is placed
        the distance from the measuring point to the camera on the z axis (depth), if the camera is placed outer then the measuring point
        this variable should be positive and if it is inner this should be negative
        :param constant: determines whether the camera data object's values are immutable (True) or mutable (False)
        """
        self.focal_length = focal_length
        self.fov = fov
        sin, cos = np.sin(yaw_angle), np.cos(yaw_angle)
        rotation_matrix = np.array([[cos, 0, sin],
                                    [0, 1, 0],
                                    [-sin, 0, cos]])
        sin, cos = np.sin(pitch_angle), np.cos(pitch_angle)
        rotation_matrix = rotation_matrix.dot(np.array([[1, 0, 0],
                                                        [0, cos, -sin],
                                                        [0, sin, cos]]))
        sin, cos = np.sin(roll_angle), np.cos(roll_angle)
        rotation_matrix = rotation_matrix.dot(np.array([[cos, -sin, 0],
                                                        [sin, cos, 0],
                                                        [0, 0, 1]]))
        self.rotation_matrix = rotation_matrix
        self.offset = np.array([x_offset, y_offset, z_offset])
        self.__is_immutable = constant

    def rotate_yaw(self, angle):
        data: CameraData = self.copy() if self.__is_immutable else self
        sin, cos = np.sin(angle), np.cos(angle)
        data.rotation_matrix = data.rotation_matrix.dot(np.array([[cos, 0, sin],
                                                                  [0, 1, 0],
                                                                  [-sin, 0, cos]]))
        return data

    def rotate_pitch(self, angle):
        data: CameraData = self.copy() if self.__is_immutable else self
        sin, cos = np.sin(angle), np.cos(angle)
        data.rotation_matrix = data.rotation_matrix.dot(np.array([[1, 0, 0],
                                                                  [0, cos, -sin],
                                                                  [0, sin, cos]]))
        return data

    def rotate_roll(self, angle):
        data: CameraData = self.copy() if self.__is_immutable else self
        sin, cos = np.sin(angle), np.cos(angle)
        data.rotation_matrix = data.rotation_matrix.dot(np.array([[cos, -sin, 0],
                                                                  [sin, cos, 0],
                                                                  [0, 0, 1]]))
        return data

    def move_x(self, x):
        data: CameraData = self.copy() if self.__is_immutable else self
        data.offset[0] += x
        return data

    def move_y(self, y):
        data: CameraData = self.copy() if self.__is_immutable else self
        data.offset[1] += y
        return data

    def move_z(self, z):
        data: CameraData = self.copy() if self.__is_immutable else self
        data.offset[2] += z
        return data

    def copy(self):
        copy = deepcopy(self)
        copy.__is_immutable = False
        return copy
