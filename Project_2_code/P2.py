import time
import math
import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def cross_product(A, B, C):
    return (B.x - A.x) * (C.y - A.y) - (B.y - A.y) * (C.x - A.x)

def merge_hulls(left_hull, right_hull):
    nL = len(left_hull)
    nR = len(right_hull)
    left_idx = nL - 1
    right_idx = 0

    done = False
    while not done:
        done = True
        while cross_product(left_hull[left_idx], right_hull[right_idx], right_hull[(right_idx + 1) % nR]) < 0:
            right_idx = (right_idx + 1) % nR
        while cross_product(right_hull[right_idx], left_hull[left_idx], left_hull[(left_idx - 1 + nL) % nL]) > 0:
            left_idx = (left_idx - 1 + nL) % nL
            done = False

    upper_left = left_idx
    upper_right = right_idx

    done = False
    left_idx = nL - 1
    right_idx = 0
    while not done:
        done = True
        while cross_product(left_hull[left_idx], right_hull[right_idx], right_hull[(right_idx - 1 + nR) % nR]) > 0:
            right_idx = (right_idx - 1 + nR) % nR
        while cross_product(right_hull[right_idx], left_hull[left_idx], left_hull[(left_idx + 1) % nL]) < 0:
            left_idx = (left_idx + 1) % nL
            done = False
    lower_left = left_idx
    lower_right = right_idx
    merged_hull = []
    idx = upper_left
    while idx != lower_left:
        merged_hull.append(left_hull[idx])
        idx = (idx + 1) % nL
    merged_hull.append(left_hull[lower_left])
    idx = lower_right
    while idx != upper_right:
        merged_hull.append(right_hull[idx])
        idx = (idx + 1) % nR
    merged_hull.append(right_hull[upper_right])
    return merged_hull

def convex_hull_rec(points, left, right):
    if right - left + 1 <= 2:
        return points[left:right + 1]

    mid = (left + right) // 2
    left_hull = convex_hull_rec(points, left, mid)
    right_hull = convex_hull_rec(points, mid + 1, right)

    return merge_hulls(left_hull, right_hull)

def convex_hull(points):
    points.sort(key=lambda p: (p.x, p.y))
    return convex_hull_rec(points, 0, len(points) - 1)

def generate_random_points(size):
    points = []
    for _ in range(size):
        points.append(Point(random.randint(0, 10000), random.randint(0, 10000)))
    return points

print(f"{'Array Size'}\t{'Theoretical Time (log base 2)'}\t{'Experimental Time (ns)'}")
print("=" * 80)

arr = [100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000, 10000000]
for size in arr:
    points = generate_random_points(size)

    start_time = time.time_ns()
    convex_hull(points)
    end_time = time.time_ns()
    experimental_time = end_time - start_time

    n_log_n = size * (math.log(size, 2))
    theoretical_time = n_log_n

    print(f"{size}\t{theoretical_time:.2f}\t{experimental_time}")
