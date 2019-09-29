from pixel_checker import is_similar_coloured_pixel

class GridPixelData:
    def __init__(self, color, px, py):
        self.color = color
        self.px = px
        self.py = py
        self.positioned = False


def convert_image_to_grid_pixel_list(pixel_image, grid_size, has_grid):
    if has_grid:
        grid_size += 1

    pixels = pixel_image.load()

    image_width = pixel_image.size[0]
    image_height = pixel_image.size[1]

    across_grid_count = image_width / grid_size
    down_grid_count = image_height / grid_size

    across_grid_index = 0
    pix_list = list()

    while across_grid_index < across_grid_count:
        center_x_pixel_pos = (grid_size * across_grid_index) + (grid_size / 2)
        down_grid_index = 0

        while down_grid_index < down_grid_count:
            center_y_pixel_pos = (grid_size * down_grid_index) + (grid_size / 2)
            grid_pixel_data = GridPixelData(pixels[center_x_pixel_pos, center_y_pixel_pos],
                                            across_grid_index, down_grid_index)
            pix_list.append(grid_pixel_data)
            down_grid_index += 1

        across_grid_index += 1
    return pix_list


def find_closest_pixel_for_colour(pixel_list, colour, current_x, current_y):

    found_pixel = None

    threshold = 0
    end_threshold =14
    shortest_move = 999999

    while threshold < end_threshold:
        for grid_pixel in pixel_list:

            pixel_positioned = grid_pixel.positioned
            matched_colour = is_similar_coloured_pixel(grid_pixel.color, colour, threshold)
            distance_to_move = calculate_distance(grid_pixel.px, grid_pixel.py, current_x, current_y)

            if not pixel_positioned and matched_colour:
                if distance_to_move < shortest_move:
                    shortest_move = distance_to_move
                    found_pixel = grid_pixel
        if found_pixel is not None:
            print
            return found_pixel

        threshold += 1
    return found_pixel


def calculate_distance(x1, y1, x2, y2):
    return abs(x1 -x2) + abs(y1 - y2)


def has_unplaced_pixels(pixel_list):

    for grid_pixel in pixel_list:
        if not grid_pixel.positioned:
            return True
    return False
