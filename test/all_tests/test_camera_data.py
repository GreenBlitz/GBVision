import unittest


class TestCameraData(unittest.TestCase):
    def test_mutable(self):
        import gbvision
        data = gbvision.CameraData(0, 0)
        data.move_x(5)
        self.assertEqual(data.offset[0], 5)

    def test_immutable(self):
        import gbvision
        data = gbvision.CameraData(0, 0, is_immutable=True)
        copy = data.move_x(5)
        self.assertEqual(data.offset[0], 0)
        self.assertEqual(copy.offset[0], 5)

    def test_rotate_mutable(self):
        import gbvision
        import numpy as np
        data = gbvision.CameraData(0, 0)
        data.rotate_yaw(np.pi)
        sin, cos = np.sin(np.pi), np.cos(np.pi)
        self.assertTrue(all(data.rotation_matrix.flatten() == np.array(np.array([[cos, 0, sin],
                                                                                 [0, 1, 0],
                                                                                 [-sin, 0, cos]])).flatten()))

    def test_rotate_immutable(self):
        import gbvision
        import numpy as np
        data = gbvision.CameraData(0, 0, is_immutable=True)
        copy = data.rotate_yaw(np.pi)
        sin, cos = np.sin(np.pi), np.cos(np.pi)
        self.assertTrue(all(copy.rotation_matrix.flatten() == np.array(np.array([[cos, 0, sin],
                                                                                 [0, 1, 0],
                                                                                 [-sin, 0, cos]])).flatten()))
