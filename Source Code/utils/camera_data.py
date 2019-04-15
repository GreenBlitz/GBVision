class CameraData:
    """
    describes constant about a camera in it's default state used to approximate distance
    between the camera and an object seen in a frame
    """
    def __init__(self, focal_length, fov):
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
        """
        self.focal_length = focal_length
        self.fov = fov

    def __copy__(self):
        return CameraData(self.focal_length, self.fov)

    copy = __copy__
