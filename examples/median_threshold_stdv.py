import unittest
from glob import glob
from pickle import load
from typing import Tuple, List

from cv2 import imread
import gbvision as gbv
import numpy as np

IMAGES_PATH = 'threshold_images/'
THRESHOLDS_PATH = 'threshold_images/results/'


class TestAutomaticThreshold(unittest.TestCase):

	def test_images(self):
		images = glob(f"{IMAGES_PATH}*.png")
		accuracies = []
		for path in images:
			image = imread(IMAGES_PATH + path)
			image_result = imread(THRESHOLDS_PATH + path)
			bbox = load(path.replace('.png', '.p'))

			thresh = find_threshold(image, bbox)
			thresh_func = gbv.ColorThreshold(thresh, 'HSV')
			result = thresh_func(image)

			accuracy = sum(abs(result - image_result)) / (len(result) * len(result[0]))
			print(f"{path} accuracy: {1 - accuracy}")
			assert accuracy < 0.1
			print("test passed\n")
			accuracies.append(sum(abs(result - image_result)))

		avg_accuracy = sum(accuracies) / len(accuracies)
		print(f"Average accuracy: {avg_accuracy}")
		assert avg_accuracy < 0.05


def find_threshold(image: np.ndarray, bbox: np.ndarray) -> List[Tuple[int, int] * 3]:
	pass
