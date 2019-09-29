import unittest

from PIL import Image

from hamapi.functions.grid_calculator import calculate_average_grid_size
from hamapi.functions.grid_calculator import calculate_grid_size
from hamapi.functions.grid_calculator import has_onepixel_grid
from hamapi.functions.grid_pixel_data import convert_image_to_grid_pixel_list


class TestCalculateGridSizeFunctions(unittest.TestCase):

    def test_calculate_grid_size_when_incolouredgrid_then_grid_calculated(self):
        img = Image.open("test_resources/images/streetfighter_vega.png")
        pix = img.load()

        self.assertEqual(calculate_grid_size(pix, 81, 75, img.size[0], img.size[1]), 20)

    def test_calculate_grid_size_when_ongridline_then_grid_notcalculated(self):
        img = Image.open("test_resources/images/streetfighter_vega.png")
        pix = img.load()

        grid_size_result = calculate_grid_size(pix, 252, 318, img.size[0], img.size[1])
        self.assertEqual(grid_size_result, -1)

    def test_calculate_average_grid_size_when_high_samplesize_then_average_calculated(self):
        img = Image.open("test_resources/images/streetfighter_vega.png")
        pix = img.load()

        grid_size_result = calculate_average_grid_size(pix, img.size, 99)
        self.assertEqual(grid_size_result, 20)

    def test_has_onepixel_grid_when_gridpresent_then_returns_true(self):
        img = Image.open("test_resources/images/streetfighter_vega.png")
        pix = img.load()

        grid_size_result = has_onepixel_grid(pix, 20, img.size[0], img.size[1])
        self.assertTrue(grid_size_result)


    def test_convert_image_to_grid_pixel_list(self):
        img = Image.open("test_resources/images/colours_4x4.png")

        grid_pixel_list = convert_image_to_grid_pixel_list(img, 20, True)
        self.assertEqual(len(grid_pixel_list), 16)


if __name__ == '__main__':
    unittest.main()