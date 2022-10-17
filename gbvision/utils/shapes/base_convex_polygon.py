import numpy as np
import cv2

from .base_polygon import BasePolygon
from gbvision.constants.types import Polygon, Contour


class BaseConvexPolygon(BasePolygon):
    @staticmethod
    def collision(shape1: Polygon, shape2: Polygon) -> bool:
        shape1, shape2 = np.array(shape1), np.array(shape2)
        shape1 = shape1.reshape(shape1.size // 2, 2)
        shape2 = shape2.reshape(shape1.size // 2, 2)

        projection_axises = []

        negation_array = np.array([-1.0, 1.0])

        for i in range(len(shape1)):
            projection_axises.append(shape1[(i + 1) % len(shape1)] - shape1[i])
        for i in range(len(shape2)):
            projection_axises.append(shape2[(i + 1) % len(shape2)] - shape2[i])

        for i in range(len(projection_axises)):
            projection_axises[i] = projection_axises[i][::-1] * negation_array

        for axis in projection_axises:
            proj1 = []
            for vertix in shape1:
                proj1.append(vertix.dot(axis))
            proj1 = min(proj1), max(proj1)

            proj2 = []
            for vertix in shape2:
                proj2.append(vertix.dot(axis))
            proj2 = min(proj2), max(proj2)

            if proj1[0] > proj2[1] or proj2[0] > proj1[1]:
                return False

        return True

    @staticmethod
    def from_contour(cnt: Contour, arc_length_multiplier=0.05) -> Polygon:
        polygon = BasePolygon.from_contour(cnt, arc_length_multiplier)
        return cv2.convexHull(polygon)
