import numpy as np
import os
from PIL import Image
from typing import Dict


def _loadfont(font: str) -> Dict[str, any]:
    path = './SRL-Fonts/{}/'.format(font)
    fnames = [fname for fname in os.listdir(path) if '.bmp' in fname]
    raws = [np.array(Image.open(path + fname)) for fname in fnames]
    return {chr(int(fname[:-4])): raw for fname, raw in zip(fnames, raws)}


def _loadfonts(fontdir: str = './SRL-Fonts/') -> Dict[str, Dict[str, any]]:
    loaded = {}
    fontnames = os.listdir(fontdir)
    for name in fontnames:
        if name[0] != '.':  # ignore dotfiles
            loaded[name] = _loadfont(name)
    return loaded


FONTS = _loadfonts()
