import unittest
import time
import core.capture as capture
import core.color as color
from core.types.cts import CTS2
from PIL import Image


class TestClass(unittest.TestCase):

    def test_capture(self):  # test core/capture.py
        # TODO: launch runelite automatically
        # self.assertTrue(capture.is_window("RuneLite"))
        cp = capture.Capture("RuneLite")
        cp.start()
        time.sleep(1)
        img = cp.get_image()
        cp.terminate()
        self.assertNotEqual(img, None)
        self.assertGreater(len(img), 0)

    def test_find_colors(self):  # test core/color.py
        img = Image.open('test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pa = color.find_colors(img, cts)
        self.assertEqual(len(pa), 2595)

    def test_pa_cluster(self):  # test core/types/point_array.py
        img = Image.open('test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pa = color.find_colors(img, cts)
        pa2d = pa.cluster(5)
        self.assertEqual(len(pa2d), 5)

    def test_pa2d_filter(self):  # test core/types/point_array2d.py
        img = Image.open('test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pa = color.find_colors(img, cts)
        pa2d = pa.cluster(5)
        pa2d = pa2d.filtersize(6, 2000)
        self.assertEqual(len(pa2d), 3)


if __name__ == '__main__':
    unittest.main()
