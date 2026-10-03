import math
from typing import List, Tuple


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def bezier_point(points, t):
    pts = [list(p) for p in points]
    n = len(pts)
    for r in range(1, n):
        for i in range(n - r):
            pts[i][0] = (1 - t) * pts[i][0] + t * pts[i + 1][0]
            pts[i][1] = (1 - t) * pts[i][1] + t * pts[i + 1][1]
    return pts[0]


def bezier_length(points, steps=200):
    length = 0.0
    prev = bezier_point(points, 0)
    for i in range(1, steps + 1):
        t = i / steps
        cur = bezier_point(points, t)
        length += distance(prev, cur)
        prev = cur
    return length


def calculate_slider_length(curve_type, start, points):
    all_points = [start] + points
    if curve_type.upper() == "L":
        return sum(
            distance(all_points[i], all_points[i + 1])
            for i in range(len(all_points) - 1)
        )
    elif curve_type.upper() == "B":
        return bezier_length(all_points)
    else:
        raise NotImplementedError("Zatím umím jen L a B")
