import unittest
import time
import core.capture as capture
import core.color as color
import core.types.point_array as pa
import core.types.point_array2d as pa2d
from core.types.cts import CTS2
from core.debug import draw_pa2d
from PIL import Image
import numpy as np


imgshow = True


class TestClass(unittest.TestCase):

    def test_capture(self):  # test core/capture.py
        # TODO: launch runelite automatically
        # self.assertTrue(capture.is_window("RuneLite"))
        cp = capture.Capture("RuneLite")
        cp.start()
        time.sleep(1)
        img = cp.get_image()
        cp.terminate()
        self.assertNotEqual(len(img), 0)
        self.assertGreater(len(img), 0)

    def test_find_colors(self):  # test core/color.py
        img = Image.open('test.jpeg')
        arr = np.array(img)
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = color.find_colors(arr, cts)
        self.assertEqual(len(pts), 2560)

    def test_pa_cluster(self):  # test core/types/point_array.py
        img = Image.open('test.jpeg')
        arr = np.array(img)
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = color.find_colors(arr, cts)
        clusters = pa.cluster(pts)
        drawn = draw_pa2d(np.array(img), clusters)
        if imgshow:
            Image.fromarray(drawn).show()
        self.assertEqual(len(clusters), 5)

    def test_pa2d_filter(self):  # test core/types/point_array2d.py
        img = Image.open('test.jpeg')
        arr = np.array(img)
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = color.find_colors(arr, cts)
        clusters = pa.cluster(pts)
        filtered = pa2d.filtersize(clusters, 50, 3000)
        drawn = draw_pa2d(arr, filtered)
        if imgshow:
            Image.fromarray(drawn).show()
        self.assertEqual(len(filtered), 1)


if __name__ == '__main__':
    unittest.main()
