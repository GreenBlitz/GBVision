import numpy as np
from copy import deepcopy

from gbvision.constants.types import Number


class CameraData:
    """
    describes constant about a camera in it's default state used to approximate distance
    between the camera and an object seen in a frame

    :param focal_length: the focal length of the camera at it's default state, in units of pixels
        can be described as the square root of the amount of pixels an object takes on a frame, multiplied by it's
        distance from the camera and divided by the square root of it's surface

        FOCAL_LENGTH = :math:' sqrt(P) * D / sqrt(S)'

        where P is the amount of pixels in the frame representing the object,
        D is the real life distance between the object and the camera
        S is the real life surface area (in 2d projection) of the object
        note that this is a constant, whatever object you choose to use, this formula will yield the same result
    :param fov_width:
        half the viewing angle of the camera (field of view) in radians, can be calculated by placing an object in front
        of the camera, so that the entire object is captured and it's center is at the frame's center.
        the tangent of the angle can be described as the width of the object in real life, divided by the
        product of the object's distance from the camera in real life and the ratio between the width of the frame
        in pixels and the width of the object in the frame, also in pixels

        math:: tan(FOV) = (Wm) / (D * (Wp/Wf))

        where Wm is the real life width of the object
        D is the real life distance between the object and the camera
        Wp is the width of the object in the frame (pixels unit)
        Wf is the width of the frame (pixels unit)
        to calculate the FOV just apply the inverse tangent

        FOV = math:: arctan(tan(FOV))

    :param fov_height:
        same as fov_width but on the height/y axis

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
    :param is_immutable: determines whether the camera data object's values are immutable (True) or mutable (False)
    """

    def __init__(self, focal_length, fov_width, fov_height, pitch_angle=0, yaw_angle=0, roll_angle=0, x_offset=0, y_offset=0, z_offset=0,
                 is_immutable=False, name=None):
        self.focal_length = focal_length
        self.fov_width = fov_width
        self.fov_height = fov_height
        self.rotation_angles = np.array([pitch_angle, yaw_angle, roll_angle])
        self.rotation_matrix = self.__calculate_rotation_matrix()
        self.offset = np.array([x_offset, y_offset, z_offset])
        self.name = name
        self.__is_immutable = is_immutable

    def __calculate_rotation_matrix(self):

        pitch_angle, yaw_angle, roll_angle = self.rotation_angles
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
        return rotation_matrix

    def __get_data(self) -> 'CameraData':
        return self.copy() if self.__is_immutable else self

    def rotate_pitch(self, angle: float) -> 'CameraData':
        """
        rotates the camera's angle around the pitch axis (the x axis)

        :param angle: the rotation angle
        :return: a camera data instance with the same params as this but with the pitch angle rotated \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.rotation_angles[0] += angle
        sin, cos = np.sin(angle), np.cos(angle)
        data.rotation_matrix = data.rotation_matrix.dot(np.array([[1, 0, 0],
                                                                  [0, cos, -sin],
                                                                  [0, sin, cos]]))
        return data

    def rotate_yaw(self, angle: float) -> 'CameraData':
        """
        rotates the camera's angle around the yaw axis (the y axis)

        :param angle: the rotation angle
        :return: a camera data instance with the same params as this but with the yaw angle rotated \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.rotation_angles[1] += angle
        sin, cos = np.sin(angle), np.cos(angle)
        data.rotation_matrix = data.rotation_matrix.dot(np.array([[cos, 0, sin],
                                                                  [0, 1, 0],
                                                                  [-sin, 0, cos]]))
        return data

    def rotate_roll(self, angle: float) -> 'CameraData':
        """
        rotates the camera's angle around the roll axis (the z axis)

        :param angle: the rotation angle
        :return: a camera data instance with the same params as this but with the roll angle rotated \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.rotation_angles[2] += angle
        sin, cos = np.sin(angle), np.cos(angle)
        data.rotation_matrix = data.rotation_matrix.dot(np.array([[cos, -sin, 0],
                                                                  [sin, cos, 0],
                                                                  [0, 0, 1]]))
        return data

    def set_pitch_angle(self, angle: float) -> 'CameraData':
        """
        sets the camera's angle around the pitch axis (the x axis)

        :param angle: the rotation angle
        :return: a camera data instance with the same params as this but with the pitch angle changed \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.rotation_angles[0] = angle
        data.rotation_matrix = data.__calculate_rotation_matrix()
        return data

    def set_yaw_angle(self, angle: float) -> 'CameraData':
        """
        sets the camera's angle around the yaw axis (the y axis)

        :param angle: the rotation angle
        :return: a camera data instance with the same params as this but with the yaw angle changed \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.rotation_angles[1] = angle
        data.rotation_matrix = data.__calculate_rotation_matrix()
        return data

    def set_roll_angle(self, angle: float) -> 'CameraData':
        """
        sets the camera's angle around the roll axis (the z axis)

        :param angle: the rotation angle
        :return: a camera data instance with the same params as this but with the roll angle changed \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.rotation_angles[2] = angle
        data.rotation_matrix = data.__calculate_rotation_matrix()
        return data

    def move_x(self, x: Number) -> 'CameraData':
        """
        moves this camera data's x axis offset

        :param x: the x offset to move by
        :return: a camera data instance with the same params as this but with the x axis moved \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.offset[0] += x
        return data

    def move_y(self, y: Number) -> 'CameraData':
        """
        moves this camera data's y axis offset

        :param y: the y offset to move by
        :return: a camera data instance with the same params as this but with the y axis moved \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.offset[1] += y
        return data

    def move_z(self, z: Number) -> 'CameraData':
        """
        moves this camera data's z axis offset

        :param z: the z offset to move by
        :return: a camera data instance with the same params as this but with the z axis moved \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.offset[2] += z
        return data

    def set_x_offset(self, x: Number) -> 'CameraData':
        """
        sets this camera data's x axis offset

        :param x: the new x offset
        :return: a camera data instance with the same params as this but with the x axis changed \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.offset[0] = x
        return data

    def set_y_offset(self, y: Number) -> 'CameraData':
        """
        sets this camera data's y axis offset

        :param y: the new y offset
        :return: a camera data instance with the same params as this but with the y axis changed \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.offset[1] = y
        return data

    def set_z_offset(self, z: Number) -> 'CameraData':
        """
        sets this camera data's z axis offset

        :param z: the new z offset
        :return: a camera data instance with the same params as this but with the z axis changed \
            if this is immutable it will return a copy of this, otherwise it will modify this instance and return it
        """
        data = self.__get_data()
        data.offset[2] = z
        return data

    def copy(self) -> 'CameraData':
        """
        creates a mutable copy of this and returns it
        :return:
        """
        copy = deepcopy(self)
        copy.__is_immutable = False
        return copy

    def is_immutable(self) -> bool:
        """
        checks if this camera data instance is immutable

        :return: True if this is immutable, False otherwise
        """
        return self.__is_immutable

    def as_immutable(self) -> 'CameraData':
        """
        creates and returns an immutable copy of this camera data
        if this instance is already immutable it will return this instance

        :return: an instance of CameraData, with the same values as this instance but immutable
        """
        if self.__is_immutable:
            return self
        copy = self.copy()
        copy.__is_immutable = True
        return copy

    def __str__(self):
        if self.name is not None:
            return f'{self.name}'
        return object.__str__(self)

    def __repr__(self):
        return str(self)
