from typing import Union, List
from .stream_camera import Camera, StreamCamera


class CameraList(Camera):
    """
    behaves as both a camera and a list of cameras
    camera list holds in it a list of cameras referenced as the field cameras
    and also a single camera to be the current camera used for every operation on the camera list
    as a single camera

    :param cameras: list of the cameras which will be part of the camera list
        you can also add and remove cameras later using the
    :param select_cam: optional, an initial camera to be selected, if not set default camera is the first
        one in the list
    """

    def __init__(self, cameras: List[Camera], select_cam: int = None):
        self.cameras: List[Camera] = cameras.copy()
        if select_cam is None and len(cameras) > 0:
            select_cam = 0
        self.selected_camera: Union[Camera, StreamCamera] = self.cameras[select_cam] if select_cam is not None else None

    def __getitem__(self, item: int) -> Camera:
        """
        returns the camera at the index
        :param item: the index
        :return: the camera
        """
        return self.cameras[item]

    def __setitem__(self, item: int, value: Camera):
        """
        sets the camera at the index to the new camera
        :param item: the index
        :param value: the new camera
        """
        self.cameras[item] = value

    def select_camera(self, index: int):
        """
        sets the selected camera to be the camera at the index
        :param index: the new selected camera's index
        """
        self.selected_camera = self.cameras[index]

    def __delitem__(self, item: int):
        """
        deletes the camera at the index
        :param item:
        """
        if self.selected_camera is self.cameras[item]:
            self.selected_camera = None
        del self.cameras[item]

    def __iter__(self):
        """
        :return: an iterator that iterates through all the cameras
        """
        return iter(self.cameras)

    def __len__(self):
        return len(self.cameras)

    def read(self, image=None, foreach=False):
        if foreach:
            return (cam.read(image=image) for cam in self.cameras)
        return self.selected_camera.read(image=image)

    def is_opened(self, foreach=False):
        if foreach:
            return (cam.is_opened() for cam in self.cameras)
        return self.selected_camera.is_opened()

    def add_camera(self, cam: Camera):
        """
        adds a new camera to the end of the list
        :param cam: the new camera
        """
        self.cameras.append(cam)

    def release(self, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.release()
        else:
            self.selected_camera.release()
            self.selected_camera = None

    def default(self):
        """
        sets the selected camera to the default camera (first camera in the list)
        """
        self.selected_camera = self.cameras[0] if len(self.cameras) > 0 else None

    def set_exposure(self, exposure, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_exposure(exposure)
        else:
            return self.selected_camera.set_exposure(exposure)

    def set_auto_exposure(self, exposure, foreach=False) -> bool:
        if foreach:
            for cam in self.cameras:
                cam.set_exposure(exposure)
        else:
            return self.selected_camera.set_exposure(exposure)

    def toggle_auto_exposure(self, auto, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_auto_exposure(auto)
        else:
            return self.selected_camera.set_auto_exposure(auto)

    @property
    def get_data(self):
        return self.selected_camera.get_data()

    def resize(self, x_factor, y_factor, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.resize(x_factor, y_factor)
        else:
            self.selected_camera.resize(x_factor, y_factor)

    def rescale(self, factor, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.rescale(factor)
        else:
            self.selected_camera.rescale(factor)

    def set_frame_size(self, width, height, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_frame_size(width, height)
        else:
            self.selected_camera.set_frame_size(width, height)

    def toggle_stream(self, should_stream, foreach=False):
        if foreach:
            for cam in self.cameras:
                if isinstance(cam, StreamCamera):
                    cam.toggle_stream(should_stream)
        else:
            if isinstance(self.selected_camera, StreamCamera):
                self.selected_camera.toggle_stream(should_stream)

    def is_streaming(self, foreach=False):
        if foreach:
            return (cam.is_streaming() if isinstance(cam, StreamCamera) else False for cam in self.cameras)
        return self.selected_camera.is_streaming()

    def get_width(self, foreach=False):
        if foreach:
            return (cam.get_width() for cam in self.cameras)
        return self.selected_camera.get_width()

    def get_height(self, foreach=False):
        if foreach:
            return (cam.get_height() for cam in self.cameras)
        return self.selected_camera.get_height()

    def _set_width(self, width: int, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam._set_width(width)
        else:
            self.selected_camera._set_width(width)

    def _set_height(self, height: int, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam._set_height(height)
        else:
            self.selected_camera._set_height(height)
