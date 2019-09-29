import random
from pixel_checker import is_similar_coloured_pixel


def has_onepixel_grid(pixelImage, grid_size, mx, my):
    mid_first_grid = round(grid_size / 2, 0)
    black = (0, 0, 0)
    threshold = 5

    for x in range(0, mx, grid_size + 1):
        if not is_similar_coloured_pixel(pixelImage[x, mid_first_grid], black, threshold):
            return False
    for y in range(0, my, grid_size + 1):
        if not is_similar_coloured_pixel(pixelImage[mid_first_grid, y], black, threshold):
            return False
    return True


def calculate_grid_size(pixelImage, sx, sy, mx, my):
    start_pixel = pixelImage[sx, sy]

    left_pixel = pixelImage[sx - 1, sy]
    left_count = 0

    similarity_threshold = 5

    while sx - left_count - 2 >= 0 and is_similar_coloured_pixel(start_pixel, left_pixel, similarity_threshold):
        left_count += 1
        left_pixel = pixelImage[sx - left_count - 1, sy]

    right_pixel = pixelImage[sx + 1, sy]
    right_count = 0

    while sx + right_count + 2 < mx and is_similar_coloured_pixel(start_pixel, right_pixel, similarity_threshold):
        right_count += 1
        right_pixel = pixelImage[sx + right_count + 1, sy]

    up_pixel = pixelImage[sx, sy - 1]
    up_count = 0

    while sy - up_count - 2 >= 0 and is_similar_coloured_pixel(start_pixel, up_pixel, similarity_threshold):
        up_count += 1
        up_pixel = pixelImage[sx, sy - up_count - 1]

    down_pixel = pixelImage[sx, sy + 1]
    down_count = 0

    while sy + down_count + 2 < my and is_similar_coloured_pixel(start_pixel, down_pixel, similarity_threshold):
        down_count += 1
        down_pixel = pixelImage[sx, sy + down_count + 1]

    if left_count + right_count == up_count + down_count:
        start_pixel = 1
        return start_pixel + left_count + right_count
    else:
        return -1


def calculate_average_grid_size(pixel_image, img_size, sample_count):
    image_width = img_size[0]
    image_height = img_size[1]

    min_expected_grid_size = 5
    max_expected_grid_size = 50

    sampled_count = 0
    sampled_count_total = 0

    for x in range(0, sample_count):
        rx = random.randint(1, image_width - 2)
        ry = random.randint(1, image_height - 2)
        grid_size = calculate_grid_size(pixel_image, rx, ry, image_width, image_height)
        if min_expected_grid_size < grid_size < max_expected_grid_size:
            sampled_count_total += grid_size
            sampled_count += 1

    if sampled_count > 0:
        return int(round(sampled_count_total / sampled_count))
    else:
        return -1
