# stuff for debugging color finding routines
import numpy as np
from PIL import Image
from typing import List
RED = np.array([255, 0, 0], dtype="uint8")


# draw point array
def draw_pa(arr: np.ndarray, pts: np.ndarray, color=RED) -> Image:
    arr = np.copy(arr)
    for p in pts:
        arr[p[0], p[1]] = color
    return arr


# draw 2d point array with random colors
def draw_pa2d(arr: np.ndarray, clusters: List[np.ndarray]) -> Image:
    arr = np.copy(arr)
    for c in clusters:
        color = np.random.randint(0, 255, 3, dtype="uint8")
        for p in c:
            arr[p[0], p[1]] = color
    return arr
