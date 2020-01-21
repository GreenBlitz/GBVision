from unittest import TestCase


class TestPipeLine(TestCase):
    def test_pipeline_calling(self):
        import gbvision as gbv
        pipeline = gbv.PipeLine(lambda x: x + 1)
        self.assertEqual(pipeline(5), 6)
        self.assertEqual(pipeline(4), 5)

    def test_pipeline_piping(self):
        import gbvision as gbv
        pipe1 = gbv.PipeLine(lambda x: x + 1)
        pipe2 = gbv.PipeLine(lambda x: x * 2)
        pipeline = pipe1 + pipe2
        self.assertEqual(pipeline(5), 12)
        self.assertEqual(pipeline(8), 18)

    def test_pipeline_multiple_init(self):
        import gbvision as gbv
        pipeline = gbv.PipeLine(lambda x: x + 1, lambda x: x * 2)
        self.assertEqual(pipeline(5), 12)
        self.assertEqual(pipeline(0), 2)
