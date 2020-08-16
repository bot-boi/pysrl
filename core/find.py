# functions for reading text from screen
# ie uptext, npc text, etc
# fonts are from SRL-Fonts on github
# char file names/ids are ascii values
# yellow chars = (255, 255, 0)
# white chars = (255, 255, 255)
import numpy as np
import numpy.ma as ma
import cv2
import os
from typing import List, Dict
from pysrl.core.types.box import Box
from pysrl.core.types.cts import CTS
from pysrl.core.types.image import Image


def colors(img: Image, color: CTS, bounds=None) -> np.ndarray:
    """
    Find locations of pixels in an image within a color range.

    Parameters
    ----------
        img : np.ndimgay
            the image to be searched
        color : CTS1 or CTS2
            the color range to capture
        bounds : Box
            the area of the image to search

    Returns
    -------
        points : np.ndimgay
            a list of points that fall in color range

    """
    (h, w, _) = np.shape(img)
    if bounds is None:
        bounds = Box.from_array([0, 0, w, h])
    b = bounds
    img = img[b.y0:b.y1, b.x0:b.x1]  # apply bounds
    x, y = np.where(np.logical_and(np.all(img <= color.max, 2),
                                   np.all(img >= color.min, 2)))
    points = np.column_stack((x, y))
    return points


def _loadfont(font: str) -> Dict[str, np.ndarray]:
    path = './SRL-Fonts/{}/'.format(font)
    fnames = [fname for fname in os.listdir(path) if '.bmp' in fname]
    raws = [Image.open(path + fname) for fname in fnames]
    return {chr(int(fname[:-4])): raw for fname, raw in zip(fnames, raws)}


def image(needle: Image, haystack: Image) -> List[Box]:
    """
    Find an image (exactly) within another image.

    Parameters
    ----------
        needle
            the image to be found
        haystack
            the image to be looked in

    Returns
    -------
        matches
            bounding boxes around any matches

    """
    matches = []
    # NOTE: height is number of rows, width is number of columns DUH
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
            if np.all(needle == haystack[y:y+sheight, x:x+swidth]):
                matches.append(Box.from_array([x, y, x+swidth, y+sheight]))
    return matches


def imagecv2(template: Image, target: Image,
             threshold: float = 0.8,
             method=cv2.TM_CCOEFF_NORMED) -> List[Box]:
    """
    Find an image (template) in another image using cv2.

    Parameters
    ----------
        template
            The image to be found.
        target
            The image to be found in.
        threshold
            How closely the template should match (0-1.0).
        method
            The method cv2 uses to compare template to source.

    Returns
    -------
        matches: List[Box]
            bounding boxes around any matches

    """
    template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
    h, w, _ = template.shape
    res = cv2.matchTemplate(target, template, method)
    loc = np.where(res >= threshold)
    matches = []
    for pt in zip(*loc):
        matches.append(Box.from_array([pt[0], pt[1], pt[0] + w, pt[1] + h]))
    return matches


# TODO: figure out why this works with yellow text
# TODO: fix bug (try finding 'New' in login-slice.png for example)
def text(txt, target: Image, fontname="UpChars07") -> List[Box]:
    """
    Find text in an image using a certain font.

    Parameters
    ----------
        txt : str
            The text to be found.
        target
            The image to search for text in.
        fontname : str
            Font to use.  See the SRL-Fonts directory for options.

    Returns
    -------
        matches: List[Box]
            location data of text

    """
    target = ma.array(target, mask=target != [255, 255, 255])
    font = _loadfont(fontname)
    height = font['a'].shape[0]
    txtimg = np.zeros((height, 1, 3), dtype='uint8')
    for c in txt:
        txtimg = np.concatenate((txtimg, font[c]), axis=1)
    txtimg = Image(txtimg)
    return image(txtimg, target)
