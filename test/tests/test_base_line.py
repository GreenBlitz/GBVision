import unittest


class TestBaseLine(unittest.TestCase):
    def test_collision(self):
        import gbvision as gbv

        line1 = ((-1, -1), (1, 1))
        line2 = ((-1, 1), (1, -1))
        self.assertTrue(gbv.BaseLine.collision(line1, line2))

        line3 = ((-5, -5), (-4, -4))
        self.assertFalse(gbv.BaseLine.collision(line1, line3))
        self.assertFalse(gbv.BaseLine.collision(line2, line3))

        line4 = ((-100, -100), (0, 100))
        self.assertFalse(gbv.BaseLine.collision(line1, line4))
        self.assertFalse(gbv.BaseLine.collision(line2, line4))

        line5 = ((10, 10), (10, 100))
        self.assertFalse(gbv.BaseLine.collision(line4, line5))

        line6 = ((-10, -10), (-10, 100))
        self.assertTrue(gbv.BaseLine.collision(line4, line6))

        line7 = ((-15, -5), (15, -5))
        self.assertTrue(gbv.BaseLine.collision(line6, line7))

        line8 = ((15, -5), (20, -5))
        self.assertFalse(gbv.BaseLine.collision(line6, line8))
