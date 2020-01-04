# array of points -- equivalent to SRL's TPointArray
import numpy as np
import hdbscan
from core.types.point import Point
from core.types.box import Box
import time


# check if point array
def ispa(arr: np.ndarray) -> bool:
    return np.shape(arr)[1] == 2


def bounds(self) -> Box:  # return a box that contains all points in self
    return Box(self[0], self[-1])


# cluster points using HDBSCAN algorithm
def cluster(arr: np.ndarray, min_samples=4, n_jobs=-1):
    assert(ispa(arr))
    model = hdbscan.HDBSCAN(min_samples=min_samples,
                            core_dist_n_jobs=n_jobs).fit(arr)
    cols, rowsize = np.shape(arr)
    labels = model.labels_
    return [arr[labels == label] for label in np.unique(labels) if label != -1]


def middle(self):  # get mean average point
    total = Point(0, 0)
    for p in self:
        total += p
    length = len(self)
    divisor = Point(length, length)
    return total // divisor


# draw point array
def draw(arr: np.ndarray, pts: np.ndarray,
         color=np.array([255, 0, 0])) -> np.ndarray:
    arr = np.copy(arr)
    for p in pts:
        arr[p[0], p[1]] = color
    return arr
