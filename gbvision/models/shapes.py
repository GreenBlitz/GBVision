from gbvision.utils.pipeline import PipeLine
import numpy as np
import cv2


def circle_collision(center1, r1, center2, r2):
    return (center1[0] - center2[0]) ** 2 + (center1[1] - center2[1]) ** 2 < (r1 + r2) ** 2


def _filter_inner_circles(circles):
    filtered_circles = []
    for i, circle in enumerate(circles):
        circle_invalid = False
        for j in range(i):
            circle_invalid = circle_collision(circle[0], circle[1], circles[j][0], circles[j][1])
            if circle_invalid:
                break
        if not circle_invalid:
            filtered_circles.append(circle)

    return filtered_circles


filter_inner_circles = PipeLine(_filter_inner_circles)


def rect_collision(r1, r2):
    return not (r1[0] > r2[0] + r2[2] or
                r1[0] + r1[2] < r1[0] or
                r1[1] > r2[1] + r2[3] or
                r1[1] + r1[3] < r2[1])


def _filter_inner_rects(rects):
    filtered_rects = []
    for i, rect in enumerate(rects):
        rect_invalid = False
        for j in range(i):
            rect_invalid = rect_collision(rect, rects[j])
            if rect_invalid:
                break
        if not rect_invalid:
            filtered_rects.append(rect)
    return filtered_rects


filter_inner_rects = PipeLine(_filter_inner_rects)


def convex_shape_collision(shape1, shape2):
    """
    detects collision between two convex shapes
    Note: if you are uncertain if a shape is convex, use convex_hull on it, it will make it convex
    :param shape1: the first shape, as a contour
    :param shape2: the second shape, as a contour
    :return:
    """
    # shape1_lines = shape1 - np.roll(shape1, 1, axis=0)
    # shape2_lines = shape2 - np.roll(shape2, 1, axis=0)
    # shape1_normals = shape1_lines[:, :, ::-1].reshape(-1, 2, 1) * np.array([[1], [-1]])
    # shape1_normals = shape1_normals.reshape(1, *shape1_normals.shape)
    # shape2_normals = shape2_lines[:, :, ::-1].reshape(-1, 2, 1) * np.array([[1], [-1]])
    # shape2_normals = shape2_normals.reshape(1, *shape2_normals.shape)
    # dot1_1 = shape1.dot(shape1_normals)
    # dot1_2 = shape1.dot(shape2_normals)
    # dot2_1 = shape2.dot(shape1_normals)
    # dot2_2 = shape2.dot(shape2_normals)

    for shape in [shape1, shape2]:
        for idx, edge1 in enumerate(shape):
            edge2 = shape[idx % len(shape1)]

            normal = (edge1 - edge2)[::-1].T
            normal[0] = -normal[0]

            min_1 = max_1 = None
            for edge in shape1:
                projected = edge.dot(normal)[0, 0]
                if min_1 is None or projected < min_1:
                    min_1 = projected

                if max_1 is None or projected > max_1:
                    max_1 = projected

            min_2 = max_2 = None
            for edge in shape2:
                projected = edge.dot(normal)[0, 0]
                if min_2 is None or projected < min_2:
                    min_2 = projected

                if max_2 is None or projected > max_2:
                    max_2 = projected

            if max_1 < min_2 or max_2 < min_1:
                return False

    return True


def _filter_inner_convex_shapes(shapes):
    filtered_shapes = []
    for i, shape in enumerate(shapes):
        shape_invalid = False
        for j in range(i):
            shape_invalid = convex_shape_collision(shape, shapes[j])
            if shape_invalid:
                break
        if not shape_invalid:
            filtered_shapes.append(shape)
    return filtered_shapes


filter_inner_convex_shape = PipeLine(_filter_inner_convex_shapes)


def rotated_rect_collision(rr1, rr2):
    return convex_shape_collision(np.array([cv2.boxPoints(rr1)]), np.array([cv2.boxPoints(rr2)]))

def _filter_inner_rotated_rects(rotated_rects):
    filtered_rotated_rects = []
    for i, rotated_rect in enumerate(rotated_rects):
        rotated_rect_invalid = False
        for j in range(i):
            rotated_rect_invalid = rotated_rect_collision(rotated_rect, rotated_rects[j])
            if rotated_rect_invalid:
                break
        if not rotated_rect_invalid:
            filtered_rotated_rects.append(rotated_rect)
    return filtered_rotated_rects

filter_inner_rotated_rects = PipeLine(_filter_inner_rotated_rects)