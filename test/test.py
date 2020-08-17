import unittest
import os
import pysrl.core.capture as capture
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

    def test_capture_runelite(self):  # test core/capture.py
        # TODO: launch runelite automatically
        cp = capture.Capture(capture.RL_CANVAS)
        arr = cp.get_image()
        self.assertNotEqual(len(arr), 0)
        if imgshow:
            Image.fromarray(arr).show("test_capture_runelite")

    def test_capture_simplicity(self):  # test core/capture.py
        # TODO: launch simplicity client automatically
        # NOTE: this picks up RuneLite as well
        cp = capture.Capture(capture.SIMP_CANVAS)
        arr = cp.get_image()
        self.assertNotEqual(len(arr), 0)
        if imgshow:
            Image.fromarray(arr).show("test_capture_simplicity")

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
        img = Image.open('test/login.png')
        # screenshot of img
        subimg = Image.open('test/login-slice.png')
        matches = find.image(subimg, img)
        if imgshow:
            for match in matches:
                img = match.draw(img)
            img.show("test_findimage")
        self.assertEqual(len(matches), 1)

    def test_find_imagecv2(self):  # test core/find.imagecv2
        img = Image.open('test/login2.png')
        subimg = Image.open('test/login-slice.png')
        matches = find.imagecv2(subimg, img, 0.8)
        if imgshow:
            for match in matches:
                img = match.draw(img)
            img.show("test_findimagecv2")
        self.assertEqual(len(matches), 1)

    def test_find_text(self):  # test core/find.text
        timg = Image.open('test/login-slice.png')
        matches = find.text('New User', timg)
        if imgshow:
            for match in matches:
                timg = match.draw(timg)
            timg.show("test_findtext")
        self.assertEqual(len(matches), 1)
