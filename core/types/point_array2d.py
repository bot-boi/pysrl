# array of point arrays -- equivalent to SRL's T2DPointArray
import numpy as np
from typing import List


# 2dpoint array class, defines array of array of points and operations on them
# underlying data is a list in the format [pointarray0,pointarray1,etc]
def filtersize(arr, m, M):  # removes clusters outside range m/M
    return [pts for pts in arr if len(pts) > m and len(pts) < M]


def sort_by_middle(self, middle):  # sort clusters by middle -- inplace
    # sort by distance between midpoint of each point array and middle
    self.sort(key=lambda pa: pa.middle().distance_from(middle))


# draw 2d point array with random colors
def draw(arr: np.ndarray, clusters: List[np.ndarray]) -> np.ndarray:
    arr = np.copy(arr)
    for c in clusters:
        color = np.random.randint(0, 255, 3, dtype="uint8")
        for p in c:
            arr[p[0], p[1]] = color
    return arr
