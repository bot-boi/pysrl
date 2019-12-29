# stuff for debugging color finding routines
import numpy as np
from PIL import Image
from core.types.point_array import PointArray
from core.types.point_array2d import PointArray2D
RED = np.array([255, 0, 0], dtype="uint8")


# draw point array
def draw_pa(img: Image, pa: PointArray, color=RED) -> Image:
    data = np.array(img)
    for p in pa:
        data[p.x, p.y] = color
    return Image.fromarray(data)


# draw 2d point array with random colors
def draw_pa2d(img: Image, pa2d: PointArray2D) -> Image:
    for pa in pa2d:
        img = draw_pa(img, pa, np.random.randint(0, 255, 3, dtype="uint8"))
    return img
