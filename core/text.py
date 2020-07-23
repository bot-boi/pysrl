# functions for reading text from screen
# ie uptext, npc text, etc
# fonts are from SRL-Fonts on github
# char file names/ids are ascii values
import numpy as np
import os
import cv2
import string


def loadfont(font: str):
    path = '../SRL-Fonts/{}/'.format(font)
    fnames = [fname for fname in os.listdir(path) if '.bmp' in fname]
    templates = [cv2.imread(path + fname) for fname in fnames]
    return {chr(int(fname[:-4])): template for fname, template in zip(fnames, templates)}  # mask black values


def testfont(target: str, font: str):
    chars = loadfont(font)
    target = cv2.imread(target)
    for (char, template) in chars.items():
        if char in string.ascii_letters:
            h, w = template.shape[:-1]
            res = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):  # Switch collumns and rows
                cv2.rectangle(target, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)

    cv2.imshow('image', target)
    cv2.waitKey(0)
