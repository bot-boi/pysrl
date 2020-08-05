# functions for reading text from screen
# ie uptext, npc text, etc
# fonts are from SRL-Fonts on github
# char file names/ids are ascii values
# yellow chars = (255, 255, 0)
# white chars = (255, 255, 255)
import numpy as np
import numpy.ma as ma
from PIL import Image
import os
from core.types.box import Box


def _loadfont(font: str, color):
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


# def cv2image(template, threshold)


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
    target = ma.array(target, mask=target != [0, 0, 0])
    font = _loadfont(fontname)
    height = font['a'].shape[0]
    txtimg = np.zeros((height, 1, 3), dtype='uint8')
    for c in txt:
        txtimg = np.concatenate((txtimg, font[c]), axis=1)
    return image(txtimg, target)
