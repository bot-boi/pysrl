# functions for reading text from screen
# ie uptext, npc text, etc
# fonts are from SRL-Fonts on github
# char file names/ids are ascii values
# yellow chars = (255, 255, 0)
# white chars = (255, 255, 255)
import numpy as np
import numpy.ma as ma
import cv2
from PIL import Image
import os
from core.types.box import Box
from core.types.cts import CTS


def colors(arr: np.ndarray, color: CTS, bounds=None):
    """
    Find locations of pixels in an image within a color range.

    Parameters
    ----------
        arr : np.ndarray
            the image to be searched
        color : CTS1 or CTS2
            the color range to capture
        bounds : Box
            the area of the image to search

    Returns
    -------
        points : np.ndarray
            a list of points that fall in color range

    """
    (h, w, _) = np.shape(arr)
    if bounds is None:
        bounds = Box.from_array([0, 0, w, h])
    b = bounds
    arr = arr[b.y0:b.y1, b.x0:b.x1]  # apply bounds
    x, y = np.where(np.logical_and(np.all(arr <= color.max, 2), np.all(arr >= color.min, 2)))
    points = np.column_stack((x, y))
    return points


def _loadfont(font: str):
    path = './SRL-Fonts/{}/'.format(font)
    fnames = [fname for fname in os.listdir(path) if '.bmp' in fname]
    imgs = [Image.open(path + fname).convert('RGB') for fname in fnames]
    raws = [np.array(img, dtype='uint8') for img in imgs]
    return {chr(int(fname[:-4])): raw for fname, raw in zip(fnames, raws)}


def image(needle: np.ndarray, haystack: np.ndarray):
    """
    Find an image (exactly) within another image.

    Parameters
    ----------
        needle : np.ndarray
            the image to be found
        haystack : np.ndarray
            the image to be found in

    Returns
    -------
        matches : List[Box]
            location data of matches

    """
    matches = []
    swidth, sheight, _ = needle.shape
    tx, ty, _ = haystack.shape
    if swidth > tx or sheight > ty:
        raise Exception('Needle is larger than haystack.')
    for y in range(ty):  # iterate y 1st cus text travels horizontal
        if y+sheight > ty:
            break
        for x in range(tx):
            if x+swidth > tx:
                break
            if np.all(needle == haystack[x:x+swidth, y:y+sheight]):
                matches.append(Box.from_array([x, y, x+swidth, y+sheight]))
    return matches


def imagecv2(template: np.ndarray, target: np.ndarray,
             threshold: float = 0.8,
             method=cv2.TM_CCOEFF_NORMED):
    """
    Find an image (template) in another image using cv2.

    Parameters
    ----------
        template : np.ndarray
            the image to be found
        target : np.ndarray
            the image to be found in
        threshold : float
            how closely the template should match (0-1.0)
        method
            the method cv2 uses to compare template to source

    Returns
    -------
        matches: List[Box]
            bounding boxes around any matches

    """
    template = cv2.cvtColor(template, cv2.COLOR_RGB2BGR)
    target = cv2.cvtColor(target, cv2.COLOR_RGB2BGR)
    w, h = template.shape[:2]
    res = cv2.matchTemplate(target, template, method)
    loc = np.where(res >= threshold)
    matches = []
    for pt in zip(*loc):
        matches.append(Box.from_array([pt[0], pt[1], pt[0] + w, pt[1] + h]))
    return matches


# TODO: figure out why this works with yellow text
# TODO: fix bug (try finding 'New' in login-slice.png for example)
def text(txt: str, target: np.ndarray, fontname="UpChars07"):
    """
    Find text in an image using a certain font.

    Parameters
    ----------
        txt : str
            the text to be found
        target : np.ndarray
            the image to find text in
        fontname : str
            font to use (see SRL-Fonts dir for options

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
    return image(txtimg, target)
