from gbvision.utils.pipeline import PipeLine


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
                r1[1] + r1[3] > r2[1])


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
