import unittest
from os import listdir
from pickle import load

from cv2 import imread

IMAGES_PATH = 'threshold_images/'
THRESHOLDS_PATH = 'threshold_images/results/'


class TestAutomaticThreshold(unittest.TestCase):

	def test_images(self):
		images = [i for i in listdir('threshold_images') if not i.endswith('.png')]
		accuracies = []
		for path in images:
			image = imread(IMAGES_PATH + path)
			image_result = imread(THRESHOLDS_PATH + path)
			bbox = load(path.replace('.png', '.p'))
			result = find_threshold(image, bbox)

			print(f"{path} accuracy: {sum(result - image_result)}")
			accuracies.append(sum(abs(result - image_result)))

		avg_accuracy = sum(accuracies) / len(accuracies)
		print(f"Average accuracy: {avg_accuracy}")
		assert avg_accuracy < 0.05


def find_threshold(image, bbox):
	pass
