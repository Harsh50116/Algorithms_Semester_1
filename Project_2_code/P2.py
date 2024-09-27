import time
import math
import random


# Class representing a point in 2D space
class Coordinate:
    def __init__(self, x_val, y_val):
        self.x_val = x_val
        self.y_val = y_val


# Function to compute the cross product of vectors
def compute_cross_product(P1, P2, P3):
    return (P2.x_val - P1.x_val) * (P3.y_val - P1.y_val) - (P2.y_val - P1.y_val) * (P3.x_val - P1.x_val)


# Function to merge two convex hulls
def combine_hulls(left_part, right_part):
    sizeL = len(left_part)
    sizeR = len(right_part)

    idxL = sizeL - 1
    idxR = 0

    merging_done = False
    while not merging_done:
        merging_done = True
        while compute_cross_product(left_part[idxL], right_part[idxR], right_part[(idxR + 1) % sizeR]) < 0:
            idxR = (idxR + 1) % sizeR
        while compute_cross_product(right_part[idxR], left_part[idxL], left_part[(idxL - 1 + sizeL) % sizeL]) > 0:
            idxL = (idxL - 1 + sizeL) % sizeL
            merging_done = False

    top_left = idxL
    top_right = idxR

    merging_done = False
    idxL = sizeL - 1
    idxR = 0
    while not merging_done:
        merging_done = True
        while compute_cross_product(left_part[idxL], right_part[idxR], right_part[(idxR - 1 + sizeR) % sizeR]) > 0:
            idxR = (idxR - 1 + sizeR) % sizeR
        while compute_cross_product(right_part[idxR], left_part[idxL], left_part[(idxL + 1) % sizeL]) < 0:
            idxL = (idxL + 1) % sizeL
            merging_done = False

    bottom_left = idxL
    bottom_right = idxR

    merged_result = []
    idx = top_left
    while idx != bottom_left:
        merged_result.append(left_part[idx])
        idx = (idx + 1) % sizeL
    merged_result.append(left_part[bottom_left])

    idx = bottom_right
    while idx != top_right:
        merged_result.append(right_part[idx])
        idx = (idx + 1) % sizeR
    merged_result.append(right_part[top_right])

    return merged_result


# Recursive function to compute the convex hull
def recursive_convex_hull(coords, start, end):
    if end - start + 1 <= 2:
        return coords[start:end + 1]

    midpoint = (start + end) // 2
    left_hull = recursive_convex_hull(coords, start, midpoint)
    right_hull = recursive_convex_hull(coords, midpoint + 1, end)

    return combine_hulls(left_hull, right_hull)


# Main convex hull function
def convex_hull_solver(coords_list):
    coords_list.sort(key=lambda p: (p.x_val, p.y_val))
    return recursive_convex_hull(coords_list, 0, len(coords_list) - 1)


# Generate random coordinates (points) for testing
def generate_random_coordinates(size):
    coord_list = []
    for _ in range(size):
        coord_list.append(Coordinate(random.randint(0, 10000), random.randint(0, 10000)))
    return coord_list


# Test the algorithm with different input sizes
print(f"{'Size'}\t{'Estimated Time O(n log n)'}\t{'Actual Time (ns)'}")
print("=" * 80)

sizes = [100, 500, 1000, 5000, 10000, 100000, 1000000, 10000000]
for size in sizes:
    random_coords = generate_random_coordinates(size)

    start_time_ns = time.time_ns()
    convex_hull_solver(random_coords)
    end_time_ns = time.time_ns()
    execution_time_ns = end_time_ns - start_time_ns

    estimated_n_log_n = size * math.log2(size)

    print(f"{size}\t{estimated_n_log_n:.2f}\t{execution_time_ns}")
