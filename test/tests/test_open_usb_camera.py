import unittest
import gbvision as gbv


class TestOpenUSBCamera(unittest.TestCase):
    def test_connect_to_camera(self):
        camera = gbv.USBCamera(0)
        self.assertTrue(camera.is_opened())
        self.assertTrue(camera.read()[0])
