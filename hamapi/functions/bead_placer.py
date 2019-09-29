class HamaBoard:
    def __init__(self, grid_pixel_list, board_grid_across, board_grid_down):
        self.grid_pixel_list = grid_pixel_list
        self.current_x = 0
        self.current_y = 0
        for grid_pixel in self.grid_pixel_list:
            assert (grid_pixel.px <= board_grid_across), "Board not wide enough for pixel imaae {}".format(grid_pixel.px)
            assert (grid_pixel.py <= board_grid_down), "Board not tall enough for pixel imaage {}".format(grid_pixel.py)

    def is_complete(self):
        for grid_pixel in self.grid_pixel_list:
            if not grid_pixel.positioned:
                return False
        return True

    def is_incomplete(self):
        return not self.is_complete()

    def update_placement(self, grid_pixel):
        self.current_x = grid_pixel.px
        self.current_y = grid_pixel.py
        grid_pixel.positioned = True
        print "Board now x {}, y {}".format(self.current_x, self.current_y)

    def get_move_to(self, grid_pixel):
        return [
              grid_pixel.px -self.current_x,
              grid_pixel.py -self.current_y
        ]

