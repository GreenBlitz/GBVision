from .stream_camera import Camera, StreamCamera


class CameraList(StreamCamera):
    """
    behaves as both a camera and a list of cameras
    camera list holds in it a list of cameras referenced as the field cameras
    and also a single camera to be the current camera used for every operation on the camera list
    as a single camera
    """

    def __init__(self, cameras: list, select_cam: int = None):
        """
        :param cameras: list of the cameras which will be part of the camera list
        you can also add and remove cameras later using the
        :param select_cam: optional, an initial camera to be selected, if not set default camera is the first
        one in the list
        """
        self.cameras = cameras[:]
        if select_cam is None and len(cameras) > 0:
            select_cam = 0
        self.camera: Camera or StreamCamera = self.cameras[select_cam] if select_cam is not None else None

    def __getitem__(self, item: int):
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
        self.camera = self.cameras[index]

    def __delitem__(self, item: int):
        """
        deletes the camera at the index
        :param item:
        """
        if self.camera is self.cameras[item]:
            self.camera = None
        del self.cameras[item]

    def __iter__(self):
        """
        :return: an iterator that iterates through all the cameras
        """
        return iter(self.cameras)

    def read(self, image=None, foreach=False):
        if foreach:
            return [cam.read(image=image) for cam in self.cameras]
        return self.camera.read(image=image)

    def is_opened(self, foreach=False):
        if foreach:
            return list(map(lambda x: x.is_opened(), self.cameras))
        return self.camera.is_opened()

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
            self.camera.release()
            self.camera = None

    def default(self):
        """
        sets the selected camera to the default camera
        """
        self.camera = self.cameras[0] if len(self.cameras) > 0 else None

    def set_exposure(self, exposure, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_exposure(exposure)
        else:
            return self.camera.set_exposure(exposure)

    def toggle_auto_exposure(self, auto, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.toggle_auto_exposure(auto)
        else:
            return self.camera.set_auto_exposure(auto)

    @property
    def focal_length(self):
        return self.camera.focal_length

    @property
    def fov(self):
        return self.camera.fov

    @property
    def data(self):
        return self.camera.data

    def resize(self, x_factor, y_factor, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.resize(x_factor, y_factor)
        else:
            self.camera.resize(x_factor, y_factor)

    def rescale(self, factor, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.rescale(factor)
        else:
            self.camera.rescale(factor)

    def set_frame_size(self, width, height, foreach=False):
        if foreach:
            for cam in self.cameras:
                cam.set_frame_size(width, height)
        else:
            self.camera.set_frame_size(width, height)

    def toggle_stream(self, should_stream, foreach=False):
        if foreach:
            for cam in self.cameras:
                if isinstance(cam, StreamCamera):
                    cam.toggle_stream(should_stream)
        else:
            if isinstance(self.camera, StreamCamera):
                self.camera.toggle_stream(should_stream)

    def is_streaming(self, foreach=False):
        if foreach:
            return list(map(lambda x: x.is_streaming(), filter(lambda x: isinstance(x, StreamCamera), self.cameras)))
        return self.camera.is_streaming()

    @property
    def width(self):
        return self.camera.width

    @property
    def height(self):
        return self.camera.height
