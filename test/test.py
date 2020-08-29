import os
import unittest

import cv2

import pysrl.core.client as client
import pysrl.core.find as find
from pysrl.core.client import is_window
from pysrl.core.types.cts import CTS2
from pysrl.core.types.image import Image
from pysrl.util import draw_text

# setting for showing test results to user
# export IMGSHOW=True, unset IMGSHOW
imgshow = eval(os.getenv('IMGSHOW', default='False'))
if __name__ == '__main__':
    unittest.main()


class TestClass(unittest.TestCase):

    @unittest.skipIf(not is_window("RuneLite"),
                     "RuneLite is not running")
    def test_client_runelite(self):  # test core/client.py
        # TODO: launch runelite automatically
        cp = client.Client(client.RL_CANVAS)
        img = cp.get_image()
        self.assertNotEqual(len(img), 0)
        if imgshow:
            img = draw_text(img, "test_client_runelite", (0, 0))
            img.show()

    @unittest.skipIf(not is_window("sun-awt-X11-XPanelPeer"),
                     "Simplicity is not running")
    def test_client_simplicity(self):  # test core/client.py
        # TODO: launch simplicity client automatically
        # NOTE: this picks up RuneLite as well
        cp = client.Client(client.SIMP_CANVAS)
        img = cp.get_image()
        self.assertNotEqual(len(img), 0)
        if imgshow:
            img = draw_text(img, "test_client_simplicity", (0, 0))
            img.show()

    def test_find_colors(self):  # test core/color.py
        img = Image.open('test/test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(img, cts)
        if imgshow:
            img = draw_text(img, "test_find_colors", (0, 0))
            pts.draw(img).show()
        self.assertEqual(len(pts), 2560)

    def test_pa_cluster(self):  # test core/types/point_array.py
        img = Image.open('test/test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(img, cts)
        clusters = pts.cluster(2)
        if imgshow:
            img = draw_text(img, "test_pa_cluster", (0, 0))
            clusters.draw(img).show()
        self.assertGreaterEqual(len(clusters), 1)

    def test_pa2d_filter(self):  # test core/types/point_array2d.py
        img = Image.open('test/test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(img, cts)
        clusters = pts.cluster(2)
        filtered = clusters.filtersize(50, 3000)
        if imgshow:
            img = draw_text(img, "test_pa2d_filter", (0, 0))
            filtered.draw(img).show()
        self.assertEqual(len(filtered), 1)

    def test_find_image(self):  # test core/find.image
        haystack = Image.open('test/login.png')
        # screenshot of haystack
        needle = Image.open('test/login-slice.png')
        match = find.image(haystack, needle)
        if imgshow:
            haystack = draw_text(haystack, "test_find_image", (0, 0))
            haystack = match.draw(haystack)
            haystack.show()
        self.assertIsNotNone(match)

    def test_find_images(self):  # test core/find.imagecv2
        haystack = Image.open('test/login2.png')
        needle = Image.open('test/login-slice.png')
        matches = find.images(haystack, needle, threshold=0.95)
        if imgshow:
            for match in matches:
                haystack = draw_text(haystack, "test_find_images", (0, 0))
                haystack = match.draw(haystack)
            haystack.show()
        self.assertEqual(len(matches), 1)

    @unittest.skip('Skipping (too long!)')
    def test_find_image_exact(self):
        haystack = Image.open('test/login2.png')
        needle = Image.open('test/login-slice.png')
        matches = find.image_exact(haystack, needle)
        if imgshow:
            for match in matches:
                haystack = match.draw(haystack)
            haystack = draw_text(haystack, "test_find_image_exact", (0, 0))
            haystack.show()
        self.assertEqual(len(matches), 1)

    @unittest.skip('Skipping (too long!)')
    def test_find_image_exact_masked(self):
        img = Image.open('./scripts/scaperune/images/older.png')
        mmap = Image.open('./scripts/scaperune/images/minimap-border.png')
        mmap.mask = mmap == [0, 0, 0]  # mask transparent aka black values
        matches = find.image_exact(img, mmap)
        print(len(matches))
        for match in matches:
            img = match.draw(img)
        img = draw_text(img, "test_find_image_exact_masked", (0, 0))
        img.show()

    def test_find_image_masked(self):
        mmap = Image.open('test/minimap-border.png',
                          alpha_mask=True)
        img = Image.open('test/test-mmap.png')
        # cv2.TM_CCORR_NORMED didnt work here...
        match = find.image(img, mmap, method=cv2.TM_SQDIFF)
        if imgshow:
            img = draw_text(img, "test_find_image_masked", (0, 0))
            img = match.draw(img)
            img.show()
        self.assertIsNotNone(match)

    # def test_find_images_masked(self):
    #     mmap = Image.open('test/minimap-border.png',
    #                       alpha_mask=True)
    #     img = Image.open('test/test-mmap.png')
    #     # cv2.TM_CCORR_NORMED didnt work here...
    #     matches = find.images(img, mmap, threshold=25000.0, method=cv2.TM_SQDIFF)
    #     if imgshow:
    #         for match in matches:
    #             img = match.draw(img)
    #         img = draw_text(img, "test_find_image_masked", (0, 0))
    #         img.show()
    #     self.assertGreater(len(matches), 0)

    def test_find_text(self):  # test core/find.text
        img = Image.open('test/login2.png')
        match = find.text(img, 'New User')
        if imgshow:
            img = draw_text(img, "test_find_text", (0, 0))
            img = match.draw(img)
            img.show()
        self.assertIsNotNone(match)
