import numpy as np

from gbvision.models.contours import FilterContours, find_contours, sort_contours, contours_to_rotated_rects, \
    contours_to_polygons, fix_contours_shape
from gbvision.tools.list_tools import split_list
from .object_finder import ObjectFinder
from gbvision.constants.system import EMPTY_PIPELINE


class TargetPairFinder(ObjectFinder):
    """
    finds a pair of vision targets
    """

    def __init__(self, threshold_func, game_object, vt_distance=0.2866, enclosing_rect_ratio=0.549,
                 contour_min_area=0):
        """
        initializes the finder
        :param vt_distance: the distance between the centers of both vision targets
        :param enclosing_rect_ratio: the ratio between the width and height of the parallel enclosing rect of the vision
        target
        :param contour_min_area: the minimal area of a contour, used in FilterContours
        """
        ObjectFinder.__init__(self, threshold_func, game_object)
        self._full_pipeline = (EMPTY_PIPELINE +
                               threshold_func +
                               find_contours +
                               FilterContours(min_area=contour_min_area) +
                               sort_contours)
        self.__vector_distance = np.array([vt_distance / 2, 0, 0])
        self.vt_distance = vt_distance
        self.enclosing_rect_ratio = enclosing_rect_ratio

    def __call__(self, frame, camera):
        cnts = self._full_pipeline(frame)
        rects = contours_to_rotated_rects(cnts)
        polys = fix_contours_shape(contours_to_polygons(cnts))
        rects_polys = zip(rects, polys)
        left_targets_polys, right_targets_polys = split_list(
            lambda rotated_rect: rotated_rect[0][2] < -45.0, rects_polys)

        left_targets = list(map(lambda pair: pair[0], left_targets_polys))
        right_targets = list(map(lambda pair: pair[0], right_targets_polys))

        left_targets_real, right_targets_real = [], []
        for i in left_targets:
            left_targets_real.append(self.game_object.location_by_params(camera, np.sqrt(i[1][0] * i[1][1]), i[0]))
        for i in right_targets:
            right_targets_real.append(self.game_object.location_by_params(camera, np.sqrt(i[1][0] * i[1][1]), i[0]))

        target_pairs = []
        i = 0
        while i < len(left_targets_real):
            lt = left_targets_real[i]
            possibles = sorted(filter(lambda t: abs(np.linalg.norm(lt - t[1]) - self.vt_distance) < 0.2,
                                      enumerate(right_targets_real)),
                               key=lambda t: abs(np.linalg.norm(lt - t[1]) - self.vt_distance))
            for p in possibles:
                if right_targets[p[0]][0][0] < left_targets[i][0][0]:
                    target_pairs.append((lt, p[1]))
                    del left_targets[i]
                    del left_targets_real[i]
                    del left_targets_polys[i]
                    del right_targets[p[0]]
                    del right_targets_real[p[0]]
                    del right_targets_polys[p[0]]
                    i -= 1
                    break
            i += 1
        all_hatches = []
        for i in target_pairs:
            all_hatches.append(
                np.concatenate(((i[0] + i[1]) / 2,
                                np.array(
                                    [np.pi / 2 - np.arccos(
                                        max(-1, min(1, (i[0][2] - i[1][2]) / (self.vt_distance * 2))))]))))

        for i, t in enumerate(left_targets_real):
            if len(left_targets_polys[i][1]) != 4:
                print('[WARN] polydp returning %d points instead of four' % len(left_targets[i][1]))
                continue

            width, height = left_targets[i][1]
            tmp_ang = np.deg2rad(90.0 + left_targets[i][2])

            w_s = np.cos(tmp_ang) * width + np.sin(tmp_ang) * height
            h_s = np.sin(tmp_ang) * width + np.cos(tmp_ang) * height

            poly = np.array(left_targets_polys[i][1])

            sorted_polys = sorted(poly, key=lambda p: p[1])
            highest = sorted_polys[0]
            lowest = sorted_polys[3]

            sorted_polys = sorted(poly, key=lambda p: p[0])
            leftest = sorted_polys[0]
            rightest = sorted_polys[3]

            sng = np.sign(np.linalg.norm(rightest - highest) - np.linalg.norm(leftest - lowest))
            angle = sng * np.arccos(min(min(w_s / h_s, h_s / w_s) / self.enclosing_rect_ratio, 1))

            rot_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                   [0, 1, 0],
                                   [-np.sin(angle), 0, np.cos(angle)]])
            all_hatches.append(np.concatenate((t - rot_matrix.dot(self.__vector_distance), np.array([-angle]))))

        for i, t in enumerate(right_targets_real):
            if len(right_targets_polys[i][1]) != 4:
                print('[WARN] polydp returning %d points instead of four' % len(right_targets[i][1]))
                continue
            width, height = right_targets[i][1]
            tmp_ang = np.deg2rad(abs(right_targets[i][2]))

            w_s = np.cos(tmp_ang) * width + np.sin(tmp_ang) * height
            h_s = np.sin(tmp_ang) * width + np.cos(tmp_ang) * height

            poly = np.array(right_targets_polys[i][1])

            sorted_polys = sorted(poly, key=lambda p: p[1])
            highest = sorted_polys[0]
            lowest = sorted_polys[3]

            sorted_polys = sorted(poly, key=lambda p: p[0])
            leftest = sorted_polys[0]
            rightest = sorted_polys[3]

            sng = np.sign(np.linalg.norm(rightest - lowest) - np.linalg.norm(leftest - highest))
            angle = sng * np.arccos(min(min(w_s / h_s, h_s / w_s) / self.enclosing_rect_ratio, 1))

            rot_matrix = np.array([[np.cos(angle), 0, np.sin(angle)],
                                   [0, 1, 0],
                                   [-np.sin(angle), 0, np.cos(angle)]])
            all_hatches.append(np.concatenate((t + rot_matrix.dot(self.__vector_distance), np.array([-angle]))))
        all_hatches.sort(key=lambda v: np.linalg.norm(v[0:3:2]), reverse=False)
        return all_hatches
