# functions for reading text from screen
# ie uptext, npc text, etc
# fonts are from SRL-Fonts on github
# char file names/ids are ascii values
# yellow chars = (255, 255, 0)
# white chars = (255, 255, 255)
import numpy as np
import numpy.ma as ma
import cv2
from typing import List
from pysrl.core.types.box import Box
from pysrl.core.types.cts import CTS
from pysrl.core.types.image import Image
from pysrl.core.types.point import Point
from pysrl.core.types.point_array import PointArray
from .font import FONTS


def colors(img: Image, color: CTS, bounds: Box = None) -> PointArray:
    """
    Find locations of pixels in an image within a color range.

    ...

    Parameters
    ----------
        img
            the image to be searched
        color
            the color range to capture
        bounds
            the area of the image to search

    Returns
    -------
        points
            a list of points that fall in color range

    """
    (h, w, _) = img.shape
    if bounds is None:
        bounds = Box.from_array([0, 0, w, h])
    b = bounds
    img = img[b.y0:b.y1, b.x0:b.x1]  # apply bounds
    (h, w, _) = img.shape
    x, y = np.where(np.logical_and(np.all(img <= color.max, 2),
                                   np.all(img >= color.min, 2)))
    x = np.add(x, b.x0)
    y = np.add(y, b.y0)
    points = np.column_stack((x, y))
    return points.view(PointArray)


def image(haystack: Image, needle: Image,
          method=cv2.TM_CCORR_NORMED) -> Box:
    """
    Find a single image (needle) in another image using cv2.

    ...
    Parameters
    ----------
        haystack
            the image to be found in
        needle
            the image to be found
        method
            the method cv2 uses to compare needle to source

    Returns
    -------
        match
            bounding boxes around the best match

    """
    # convert to BGR because thats what OPENCV (cv2) uses
    needle = cv2.cvtColor(needle, cv2.COLOR_RGB2BGR)  # np arrays
    haystack = cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)
    h, w, _ = needle.shape
    res = cv2.matchTemplate(haystack, needle, method)
    # min/Max val, min/Max location
    mval, Mval, mloc, Mloc = cv2.minMaxLoc(res)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = Point.from_array(mloc)
    else:
        top_left = Point.from_array(Mloc)
    bot_right = Point(top_left.x + w, top_left.y + h)
    match = Box(top_left, bot_right)
    return match


def images(haystack: Image, needle: Image,
           threshold: float = 0.8,
           method=cv2.TM_CCORR_NORMED) -> List[Box]:
    """
    Find any number of images (needle) in another image using cv2.

    ...
    Parameters
    ----------
        haystack
            the image to be found in
        needle
            the image to be found
        threshold
            how closely the needle should match (0-1.0)
        method
            the method cv2 uses to compare needle to source

    Returns
    -------
        matches
            bounding boxes around any matches

    """
    # convert to BGR because thats what OPENCV (cv2) uses
    needle = cv2.cvtColor(needle, cv2.COLOR_RGB2BGR)  # np arrays
    haystack = cv2.cvtColor(haystack, cv2.COLOR_RGB2BGR)
    h, w, _ = needle.shape
    res = cv2.matchTemplate(haystack, needle, method)
    loc = np.where(res >= threshold)
    matches = []
    for x, y in zip(*loc):
        bounds = Box.from_array([x, y, x + w, y + h])
        matches.append(bounds)
    return matches


# TODO: make this fn suck less - WAY too slow, use find.imagecv2 instead
def image_exact(haystack: Image, needle: Image) -> List[Box]:
    """
    Find an image (exactly) within another image.

    Parameters
    ----------
        haystack
            the image to be looked in
        needle
            the image to be found

    Returns
    -------
        matches
            bounding boxes around any matches

    """
    matches = []
    needle = needle.copy()
    needle[np.where(needle.mask is True)] = [0, 0, 0]
    sheight, swidth, _ = needle.shape
    ty, tx, _ = haystack.shape  # total x,y
    if swidth > tx or sheight > ty:
        raise Exception('Needle is larger than haystack.')
    for y in range(ty):  # iterate y 1st cus text travels horizontal
        if y+sheight > ty:
            break
        for x in range(tx):
            if x+swidth > tx:
                break
            s_haystack = haystack.copy()[y: y + sheight, x: x + swidth]
            s_haystack[np.where(needle.mask is True)] = [0, 0, 0]
            needle.mask = False  # remove the mask cus we dont need it no more
            if np.all(needle[0, 0] == s_haystack[0, 0]):
                if np.all(needle == s_haystack):
                    match = Box.from_array([x, y, x+swidth, y+sheight])
                    matches.append(match)
    return matches


# TODO: figure out why this works with yellow text
# TODO: fix bug (try finding 'New' in login-slice.png for example)
def text(haystack: Image, text: str, fontname: str = "UpChars07") -> List[Box]:
    """
    Find text in an image using a certain font.

    ...

    Parameters
    ----------
        haystack
            The image to search for text in.
        text
            The text to be found.
        fontname : str
            Font to use.  See the SRL-Fonts directory for options.

    Returns
    -------
        matches
            location data of text

    """
    haystack = Image(ma.array(haystack, mask=haystack != [255, 255, 255]))
    font = FONTS[fontname]
    height = font['a'].shape[0]
    textimg = np.zeros((height, 1, 3), dtype='uint8')
    for c in text:
        textimg = np.concatenate((textimg, font[c]), axis=1)
    textimg = Image(textimg)
    return image(haystack, textimg)  # find.image, not Image
