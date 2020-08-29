import numpy as np
import os
from PIL import Image
from typing import Dict


def _font_path(fontdir: str) -> str:
    path = __file__.split('/')[:-1]  # split & remove filename.py
    end = path.index('pysrl') + 1  # remove dirs that occur after pysrl
    path = path[:end]
    path = '/'.join(path) + '/' + fontdir + '/'
    return path


def _loadfont(path: str) -> Dict[str, any]:
    fnames = [fname for fname in os.listdir(path) if '.bmp' in fname]
    raws = [np.array(Image.open(path + fname)) for fname in fnames]
    return {chr(int(fname[:-4])): raw for fname, raw in zip(fnames, raws)}


def _loadfonts(fontdir: str = 'SRL-Fonts') -> Dict[str, Dict[str, any]]:
    path = _font_path(fontdir)
    loaded = {}
    fontnames = os.listdir(path)
    for name in fontnames:
        if name[0] != '.':  # ignore dotfiles
            loaded[name] = _loadfont(path + name + '/')
    return loaded


FONTS = _loadfonts()
