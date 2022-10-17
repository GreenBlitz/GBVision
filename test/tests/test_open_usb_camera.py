import unittest


class TestOpenUSBCamera(unittest.TestCase):
    def test_connect_to_camera(self):
        import gbvision as gbv
        camera = gbv.USBCamera(0)
        self.assertTrue(camera.is_opened())
        self.assertTrue(camera.read()[0])
