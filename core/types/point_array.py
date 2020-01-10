# array of points -- equivalent to SRL's TPointArray
import numpy as np
import hdbscan
from core.types.point import Point
from core.types.box import Box
import sklearn


# check if point array
def ispa(arr: np.ndarray) -> bool:
    return np.shape(arr)[1] == 2


def bounds(self) -> Box:  # return a box that contains all points in self
    return Box(self[0], self[-1])


# clustering algorithm by benland100
def cluster_ben(points,radius=5):
    clusters = np.zeros(len(points),dtype='uint32')
    while True: #loop until all points are clustered
        unclustered = clusters==0
        remaining = np.count_nonzero(unclustered)
        if remaining == 0:
            break 
        # any points near this group (and their points) become a new group
        candidate = points[unclustered][np.random.randint(remaining)] #do this randomly to save time
        dist = np.sum(np.square(points-candidate),axis=1)
        nearby_mask = dist<=radius*radius #importantly includes candidate point
        overlaps = set(list(clusters[nearby_mask])) #groups that were close
        overlaps.remove(0)
        if len(overlaps) == 0:
            G = np.max(clusters)+1 #new cluster
        else:
            G = np.min(list(overlaps)) #prefer smaller numbers
        #set all nearby clusters to index G
        clusters[nearby_mask] = G
        for g in overlaps:
            if g == G or g == 0:
                continue
            clusters[clusters==g] = G
    unique, counts = np.unique(clusters, return_counts=True)
    cluster_points = np.asarray([points[clusters==c] for c in unique])
    return cluster_points,counts


# cluster points using HDBSCAN algorithm
def cluster(arr: np.ndarray, min_samples=4, n_jobs=-1):
    assert(ispa(arr))
    clusters, counts = cluster_ben(arr, 3)
    # print(len(clusters), 'counts',  counts)
    return clusters
    print(len(arr))
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
