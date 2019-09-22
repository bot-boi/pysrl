import colorsys
import numpy as np
from PIL import Image

# convert a PIL rgb PIL Image to hsl
# NOTE: does it make more sense to just convert an array and return an array?
# TODO: make multithreaded, too slow to be usable (takes seconds to finish)
def rgb_to_hsl(img):
    if img.mode != "RGB":
        raise Exception("Invalid mode {}".format(img.mode))

    data = np.array(img)
    for row in data:      # there's probably some cool way to do this iteration
        for pixel in row:
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

# use vector math to convert rgb image to hsl image
# written by benland100
def rgb2hsl(x):
    '''converts an [...,3] RGB image to an [...,3] HSL image'''
    hsl = np.empty_like(x,dtype='float32')
    x = np.asarray(x,dtype='float32')/255.0
    m = np.min(x,axis=-1)
    M = np.max(x,axis=-1)
    c = M-m
    dg = c==0
    ndg = ~dg
    r = x[...,0]
    g = x[...,1]
    b = x[...,2]
    hsl[...,2]=(M+m)/2
    hsl[ndg,1]=c[ndg]/(1.0-np.abs(2.0*hsl[ndg,2]-1.0))
    maskr = np.logical_and(np.equal(r,M),ndg)
    hsl[maskr,0] = (g[maskr] - b[maskr]) / c[maskr] / 6.0 + np.where(g[maskr] < b[maskr],1.0,0.0)
    maskg = np.logical_and(np.equal(g,M),ndg)
    hsl[maskg,0] = (b[maskg] - r[maskg]) / c[maskg] / 6.0 + 1.0/3.0
    maskb = np.logical_and(np.equal(b,M),ndg)
    hsl[maskb,0] = (r[maskb] - g[maskb]) / c[maskb] / 6.0 + 2.0/3.0
    hsl[dg,0] = 0.0
    hsl[dg,1] = 0.0
    return hsl
