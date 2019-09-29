from functions.argument_helper import get_program_arguments
from functions.grid_calculator import calculate_average_grid_size
from functions.grid_calculator import has_onepixel_grid
from functions.grid_pixel_data import *
from functions.image_loader import load_image
from functions.bead_colour_reader import  get_next_bead_color
from functions.bead_placer import HamaBoard
from functions.stepper_motor import StepperMotor
from functions.stepper_motor import setup_pins
from functions.stepper_motor import reset_pins

setup_pins()

args = get_program_arguments()

img = load_image(args.image_type, args.image_path)
pixel_image = img.load()

grid_size = calculate_average_grid_size(pixel_image, img.size, 99)
includes_1px_grid = has_onepixel_grid(pixel_image, grid_size, img.size[0], img.size[1])

grid_pixel_list = convert_image_to_grid_pixel_list(img, grid_size, includes_1px_grid)

iteration = 0
placements = 0
max_iterations = 100

hama_board = HamaBoard(grid_pixel_list, 50, 50)

x_axis_stepper_motor = StepperMotor([7,11,13,15], "X")
y_axis_stepper_motor = StepperMotor([31,33,35,37], "Y")

while hama_board.is_incomplete() and iteration < max_iterations :
    color = get_next_bead_color()
    found_pixel = find_closest_pixel_for_colour(grid_pixel_list, color, hama_board.current_x, hama_board.current_y)
    if found_pixel is not None:
        move_required = hama_board.get_move_to(found_pixel)

        x_axis_stepper_motor.move_by(move_required[0])
        y_axis_stepper_motor.move_by(move_required[1])

        hama_board.update_placement(found_pixel)
        placements += 1
    iteration += 1
print "Iterations ran: {}, placed {}".format(iteration, placements)

reset_pins()
