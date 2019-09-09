import colorsys
import numpy as np
from PIL import Image

# convert a PIL rgb PIL Image to hsl
# NOTE: does it make more sense to just convert an array and return an array?
def rgb_to_hsl(img):
    if img.mode != "RGB":
        raise Exception("Invalid mode {}".format(img.mode))

    data = np.array(img)
    for row in data:      # there's probably some cool way to do this iteration
        for col in row:   # with numpy
            for pixel in col:
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                r = r/255 # normalize
                g = g/255
                b = b/255
                h, l, s = colorsys.rgb_to_hls(r, g, b)
                pixel[0] = h
                pixel[1] = s
                pixel[2] = l

    return Image.fromarray(data)
