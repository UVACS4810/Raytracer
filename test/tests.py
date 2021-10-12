import unittest

import numpy as np
import src.utils as utils
import src.vertex as vertex


class TestVertex(unittest.TestCase):
    def test_convert_vertex_to_list(self):
        r = 255
        g, b, x, y = 0, 0, 0, 0
        p1 = vertex.Vertex(x, y, r, g, b)
        p1_as_list = utils.object_to_list(p1)
        fields = [r, g, b, x, y]
        for field in fields:
            self.assertIn(field, p1_as_list)

    def test_as_ndarray(self):
        v = vertex.Vertex(1,1)
        l = [1,1,0,0,0]
        ll = np.array(l)
        self.assertEqual(ll.all(), v.as_ndarray().all())

class TestUtils(unittest.TestCase):
    def test_convert_hex_to_rgb(self):
        hex_color = "#aaaaff"
        rgb: utils.RGB = utils.RGB(170, 170, 255)
        self.assertEqual(utils.convert_hex_to_rgb(hex_color), rgb)

        hex_color = "#aaaaff01"
        rgb: utils.RGB = utils.RGB(170, 170, 255, 1)
        self.assertEqual(utils.convert_hex_to_rgb(hex_color), rgb)

    def test_add_RGB(self):
        c1 = utils.RGB(1, 1, 1)
        c2 = utils.RGB(1, 1, 1)
        expected = utils.RGB(2, 2, 2)
        self.assertEqual(c1 + c2, expected)
        # check overflow behavior

    def test_make_filename_list(self):
        # case with one image
        expected = ["whatnot.png"]
        image_info = utils.ImageInfo(filename="whatnot.png", width=1, height=1)
        self.assertEqual(expected, utils.make_filename_list(image_info=image_info))

        expected = ["whatnot000.png"]
        image_info.filename="whatnot"
        image_info.number_of_images= len(expected)
        image_info.is_single_file = False
        self.assertEqual(expected, utils.make_filename_list(image_info=image_info))

        # case with 5 images
        expected = [
            "whatnot000.png",
            "whatnot001.png",
            "whatnot002.png",
            "whatnot003.png",
            "whatnot004.png",
        ]
        image_info.number_of_images = len(expected)
        actual = utils.make_filename_list(image_info=image_info)
        self.assertEqual(expected, actual)

    def test_line_to_list(self):
        expected = ["xyrgb", "6" ,"3", "0", "0", "0"]
        lines: list(str) = [
            'xyrgb 6 3   0 0 0',
            "xyrgb 6 3 0 0 0",
            "   xyrgb 6 3 0 0      0",
            "xyrgb 6 3 0 0 0        ",
            "    xyrgb 6 3 0 0 0        ",
        ]
        for line in lines:
            out = utils.line_to_list(line)
            self.assertEqual(out, expected)
    def test_add_add_pixl_colors(self):
        # The top pixel should take precidence when it has a full opacity
        c1 = utils.RGB(255, 255, 0, 255)
        c2 = utils.RGB(255, 0, 0, 255)
        c_result = utils.add_pixel_colors(c1, c2)
        self.assertEqual(c_result, c1)

        # The bottom pixel will take precidence when the top pixel has no opacity
        c1 = utils.RGB(255, 255, 0, 0)
        c2 = utils.RGB(255, 0, 0, 255)
        c_result = utils.add_pixel_colors(c1, c2)
        self.assertEqual(c_result, c2)

        # When they are mixed it is a little harder to determine
        c1 = utils.RGB(100, 100, 100, 100)
        c2 = utils.RGB(100, 100, 100, 100)
        expected = utils.RGB(100, 100,100, 161)
        c_result = utils.add_pixel_colors(c1, c2)
        self.assertEqual(c_result, expected)

    def test_linear_RGB_to_sRGB(self):
        linear_rgb = utils.RGBLinear(2/255.0, 20/255.0, 200/255.0)
        val1 = 0.08494473023 * 255
        val2 = 0.31027774743 * 255
        val3 = 0.89843234818 * 255
        expected_rgb = utils.RGB(val1, val2, val3)
        created_rgb = linear_rgb.as_rgb()
        self.assertAlmostEqual(expected_rgb.r, created_rgb.r)
        self.assertAlmostEqual(expected_rgb.g, created_rgb.g)
        self.assertAlmostEqual(expected_rgb.b, created_rgb.b)


        

    def test_draw_data_clear(self):
        draw_data_orig = utils.DrawData([], 1, 1)
        draw_data_updated = utils.DrawData([], 1, 1)
        draw_data_updated.color = utils.RGBLinear(1.1, 1.0, 1.0)
        self.assertNotEqual(draw_data_orig.color, draw_data_updated.color)
        draw_data_updated.clear()
        self.assertEqual(draw_data_orig.color, draw_data_updated.color)