# array of points -- equivalent to SRL's TPointArray
import numpy as np
from pysrl.core.types.point import Point
from pysrl.core.types.box import Box
# import os
# from concurrent.futures import ThreadPoolExecutor


# cpu_count = len(os.sched_getaffinity(0))
# executor = ThreadPoolExecutor(max_workers=cpu_count*2)


# check if point array
def ispa(arr: np.ndarray) -> bool:
    return np.shape(arr)[1] == 2


def bounds(points: np.ndarray) -> Box:  # return a box that contains all points in self
    mx = points[0][0]
    Mx = points[0][0]
    my = points[0][1]
    My = points[0][1]
    for p in points:
        x = p[0]
        y = p[1]
        if x < mx:
            mx = x
        elif x > Mx:
            Mx = x
        if y < my:
            my = y
        elif y > My:
            My = y
    return Box(Point(mx, my), Point(Mx, My))


# clustering algorithm by benland100
# bounds is the Box type
def cluster(points: np.ndarray, radius=5, bnds=None):
    if bnds is not None:
        points = bnds.contains(points)
    clusters = np.zeros(len(points), dtype='uint32')
    while True:  # loop until all points are clustered
        unclustered = clusters == 0
        remaining = np.count_nonzero(unclustered)
        if remaining == 0:
            break
        # any points near this group (and their points) become a new group
        # do this randomly to save time
        candidate = points[unclustered][np.random.randint(remaining)]
        dist = np.sum(np.square(points-candidate), axis=1)
        # importantly includes candidate point
        nearby_mask = dist <= radius*radius
        overlaps = set(list(clusters[nearby_mask]))  # groups that were close
        overlaps.remove(0)
        if len(overlaps) == 0:
            G = np.max(clusters)+1  # new cluster
        else:
            G = np.min(list(overlaps))  # prefer smaller numbers
        # set all nearby clusters to index G
        clusters[nearby_mask] = G
        for g in overlaps:
            if g == G or g == 0:
                continue
            clusters[clusters == g] = G
    unique, counts = np.unique(clusters, return_counts=True)
    # cluster_points = np.asarray([points[clusters == c] for c in unique])
    cluster_points = [points[clusters == c] for c in unique]
    return cluster_points  # , counts


"""
def fastcluster(points: np.ndarray, radius=5, n_jobs=None) -> np.ndarray:
    if n_jobs is None:
        n_jobs = cpu_count  # n of boxes points will be divided into
    rbox = bounds(points)  # bounding box of input points
    xint, yint = (2, 2)
    tile_w = rbox.width // xint  # tile width in pixels
    tile_h = rbox.height // yint  # tile height in pixels
    boxes = []
    boxes.append(rbox)
    for x in range(xint):
        for y in range(yint):
            b = Box.from_array([x * tile_w + rbox.x1, y * tile_h + rbox.y1,
                                (x + 1) * tile_w + rbox.x1, (y + 1) * tile_h + rbox.y1])
            boxes.append(b)
            print(b, x, y)
    futures = [executor.submit(cluster, box.contains(points), radius) for box in boxes]
    values = [v.result() for v in concurrent.futures.as_completed(futures)]
    result = []
    for v in values:
        result += v
    return result, boxes


def clustermulti(points: np.ndarray, radius=5) -> np.ndarray:
    work = np.array_split(points, cpu_count)
    futures = [executor.submit(cluster, w, radius) for w in work]
    values = [v.result() for v in concurrent.futures.as_completed(futures)]
    result = []
    for v in values:
        result += v
    return result
"""


# draw point array
def draw(arr: np.ndarray, pts: np.ndarray,
         color=np.array([255, 0, 0])) -> np.ndarray:
    arr = np.copy(arr)
    for p in pts:
        arr[p[0], p[1]] = color
    return arr
