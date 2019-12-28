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
        data.move_x(5)
        self.assertEqual(data.offset[0], 0)
