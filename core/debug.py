# stuff for debugging color finding routines
import numpy as np
from PIL import Image

# draw point array
def draw_pa(img, pa, color=np.array([255,0,0],dtype="uint8")):
    data = np.array(img)
    for p in pa:
        data[p.x,p.y] = color
    return Image.fromarray(data)

def draw_pa2d(img, pa2d):
    for pa in pa2d:
        img = draw_pa(img, pa, np.random.randint(0, 255, 3, dtype="uint8"))
    return img
