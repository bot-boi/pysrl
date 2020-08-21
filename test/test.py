import unittest
import os
import pysrl.core.client as client
import pysrl.core.find as find
from pysrl.core.types.cts import CTS2
from pysrl.core.types.image import Image
from pysrl.core.types.point_array2d import PointArray2D


# setting for showing test results to user
# export IMGSHOW=True, unset IMGSHOW
imgshow = eval(os.getenv('IMGSHOW', default='False'))
if __name__ == '__main__':
    unittest.main()


class TestClass(unittest.TestCase):

    def test_client_runelite(self):  # test core/client.py
        # TODO: launch runelite automatically
        cp = client.Client(client.RL_CANVAS)
        arr = cp.get_image()
        self.assertNotEqual(len(arr), 0)
        if imgshow:
            Image.fromarray(arr).show("test_client_runelite")

    def test_client_simplicity(self):  # test core/client.py
        # TODO: launch simplicity client automatically
        # NOTE: this picks up RuneLite as well
        cp = client.Client(client.SIMP_CANVAS)
        arr = cp.get_image()
        self.assertNotEqual(len(arr), 0)
        if imgshow:
            Image.fromarray(arr).show("test_client_simplicity")

    def test_find_colors(self):  # test core/color.py
        img = Image.open('test/test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(img, cts)
        if imgshow:
            pts.draw(img).show('test_find_colors')
        self.assertEqual(len(pts), 2560)

    def test_pa_cluster(self):  # test core/types/point_array.py
        img = Image.open('test/test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(img, cts)
        clusters = pts.cluster(2)
        if imgshow:
            clusters.draw(img).show('test_pa_cluster')
        self.assertGreaterEqual(len(clusters), 1)

    def test_pa2d_filter(self):  # test core/types/point_array2d.py
        img = Image.open('test/test.jpeg')
        cts = CTS2([0, 0, 0], 10, 10, 10)
        pts = find.colors(img, cts)
        clusters = pts.cluster(2)
        filtered = PointArray2D(clusters.filtersize(50, 3000))
        if imgshow:
            filtered.draw(img).show('test_pa2d_filter')
        self.assertEqual(len(filtered), 1)

    def test_find_image(self):  # test core/find.image
        haystack = Image.open('test/login.png')
        # screenshot of haystack
        needle = Image.open('test/login-slice.png')
        match = find.image(haystack, needle)
        if imgshow:
            haystack = match.draw(haystack)
            haystack.show("test_find_image")
        self.assertIsNotNone(match)

    def test_find_images(self):  # test core/find.imagecv2
        haystack = Image.open('test/login2.png')
        needle = Image.open('test/login-slice.png')
        matches = find.images(haystack, needle, 0.8)
        if imgshow:
            for match in matches:
                haystack = match.draw(haystack)
            haystack.show("test_find_imagecv2")
        self.assertEqual(len(matches), 1)

    def test_find_text(self):  # test core/find.text
        img = Image.open('test/login2.png')
        match = find.text(img, 'New User')
        if imgshow:
            img = match.draw(img)
            img.show("test_find_text")
        self.assertIsNotNone(match)
