#!/usr/bin/python3
import unittest
import time
import core.capture as capture
import core.types.point_array as pa
import core.types.point_array2d as pa2d
from core.types.cts import CTS2
import core.find as find
from PIL import Image
import numpy as np


# TODO: better test configuration
imgshow = False


class TestClass(unittest.TestCase):

    def test_capture_runelite(self):  # test core/capture.py
        # TODO: launch runelite automatically
        # self.assertTrue(capture.is_window("RuneLite"))
        cp = capture.Capture(capture.RL_WINDOW, capture.RL_CANVAS)
        cp.start()
        time.sleep(1)
        arr = cp.get_image()
        cp.terminate()
        self.assertNotEqual(len(arr), 0)
        self.assertGreater(len(arr), 0)
        if imgshow:
            Image.fromarray(arr).show()

    def test_capture_simplicity(self):  # test core/capture.py
        # TODO: launch runelite automatically
        # self.assertTrue(capture.is_window("RuneLite"))
        cp = capture.Capture(capture.SIMP_WINDOW, capture.SIMP_CANVAS)
        cp.start()
        time.sleep(1)
        arr = cp.get_image()
        cp.terminate()
        self.assertNotEqual(len(arr), 0)
        self.assertGreater(len(arr), 0)
        if imgshow:
            Image.fromarray(arr).show()

    def test_find_colors(self):  # test core/color.py
        img = Image.open('test.jpeg')
        arr = np.array(img)
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(arr, cts)
        if imgshow:
            drawn = pa.draw(np.array(img), pts)
            Image.fromarray(drawn).show('test_find_colors')
        self.assertEqual(len(pts), 2560)

    def test_pa_cluster(self):  # test core/types/point_array.py
        img = Image.open('test.jpeg')
        arr = np.array(img)
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(arr, cts)
        clusters = pa.cluster(pts, 2)
        if imgshow:
            drawn = pa2d.draw(np.array(img), clusters)
            Image.fromarray(drawn).show('test_pa_cluster')
        self.assertGreaterEqual(len(clusters), 1)

    def test_pa2d_filter(self):  # test core/types/point_array2d.py
        img = Image.open('test.jpeg')
        arr = np.array(img)
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(arr, cts)
        clusters = pa.cluster(pts, 2)
        filtered = pa2d.filtersize(clusters, 50, 3000)
        drawn = pa2d.draw(arr, filtered)
        if imgshow:
            Image.fromarray(drawn).show('test_pa2d_filter')
        self.assertEqual(len(filtered), 1)

    def test_findimage(self):  # test core/find.image
        img = np.array(Image.open('login.png').convert('RGB'))
        # screenshot of img
        subimg = np.array(Image.open('login-slice.png').convert('RGB'))
        matches = find.image(subimg, img)
        if imgshow:
            Image.fromarray(subimg).show()
            for match in matches:
                match.draw(img)
            Image.fromarray(img).show()
        self.assertEqual(len(matches), 1)

    def test_findimagecv2(self):  # test core/find.imagecv2
        img = np.array(Image.open('login2.png').convert('RGB'))
        subimg = np.array(Image.open('login-slice.png').convert('RGB'))
        matches = find.imagecv2(subimg, img, 0.8)
        if imgshow:
            for match in matches:
                match.draw(img)
            Image.fromarray(img).show()
        self.assertEqual(len(matches), 1)

    def test_findtext(self):  # test core/find.text
        timg = np.array(Image.open('login-slice.png').convert('RGB'))
        matches = find.text('New User', timg)
        if imgshow:
            for match in matches:
                match.draw(timg)
            Image.fromarray(timg).show()
        self.assertEqual(len(matches), 1)


if __name__ == '__main__':
    unittest.main()
else:
    unittest.main()
