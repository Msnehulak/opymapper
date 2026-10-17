import math


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


def calculate_perfect_circle_length(start, points):
    if len(points) != 2:
        raise ValueError(
            "Perfect circle slider ('P') segment musí mít v poli points přesně 2 body."
        )

    A = start
    B = points[0]
    C = points[1]

    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-9:
        raise ValueError("Body leží na jedné přímce, nelze vytvořit kružnici.")

    ux = (
        (x1**2 + y1**2) * (y2 - y3)
        + (x2**2 + y2**2) * (y3 - y1)
        + (x3**2 + y3**2) * (y1 - y2)
    ) / d
    uy = (
        (x1**2 + y1**2) * (x3 - x2)
        + (x2**2 + y2**2) * (x1 - x3)
        + (x3**2 + y3**2) * (x2 - x1)
    ) / d

    radius = math.hypot(x1 - ux, y1 - uy)

    v1 = (x1 - ux, y1 - uy)
    v2 = (x3 - ux, y3 - uy)
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    det = v1[0] * v2[1] - v1[1] * v2[0]
    total_angle = abs(math.atan2(det, dot))

    cross_b = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
    chord = math.hypot(x3 - x1, y3 - y1)

    if radius > chord / 2:
        half_angle = math.asin(min(1.0, chord / (2 * radius)))
        theta = 2 * half_angle
    else:
        theta = 2 * math.pi - 2 * math.asin(min(1.0, chord / (2 * radius)))

    return radius * theta


def parse_slider_segments(start_x, start_y, initial_curve_type, raw_points):
    segments = []
    current_curve = initial_curve_type.upper()
    current_start = (start_x, start_y)
    current_points = [current_start]

    for pt in raw_points:
        if len(pt) == 3:
            px, py, c_type = pt
            current_points.append((int(px), int(py)))
            segments.append({"curve_type": current_curve, "points": current_points})
            current_curve = c_type.upper()
            current_start = (int(px), int(py))
            current_points = [current_start]
        else:
            px, py = pt
            current_points.append((int(px), int(py)))

    if len(current_points) > 1 or not segments:
        segments.append({"curve_type": current_curve, "points": current_points})

    return segments


def calculate_slider_length(curve_type, start, points):
    segments = parse_slider_segments(start[0], start[1], curve_type, points)
    total_length = 0.0

    for seg in segments:
        c_type = seg["curve_type"]
        seg_points = seg["points"]

        if c_type == "L":
            total_length += sum(
                distance(seg_points[i], seg_points[i + 1])
                for i in range(len(seg_points) - 1)
            )
        elif c_type == "B":
            total_length += bezier_length(seg_points)
        elif c_type == "P":
            # P segment potřebuje start + 2 body (celkem 3 body v seg["points"])
            p_start = seg_points[0]
            p_points = seg_points[1:]
            if len(p_points) == 2:
                total_length += calculate_perfect_circle_length(p_start, p_points)
            else:
                # Pokud nemá přesně 2 body, fallback na lineární/bézier nebo výjimka
                total_length += sum(
                    distance(seg_points[i], seg_points[i + 1])
                    for i in range(len(seg_points) - 1)
                )
        else:
            raise NotImplementedError(f"Zatím neumím typ křivky: {c_type}")

    return total_length
