# array of points -- equivalent to SRL's TPointArray
import numpy as np
import hdbscan
from typing import List
from core.types.point_array2d import PointArray2D
from core.types.point import Point
from core.types.box import Box
import time


# point array class -- defines array of points and operations upon them
# underlying data is an array of Point
class PointArray(List):

    @classmethod  # alternate constructor, accepts numpy array w/format [[x,y]]
    def from_array(class_object, arr):
        points = []
        for p in arr:
            points.append(Point.from_array(p))
        return class_object(points)

    def as_array(self):  # returns points as numpy array -- [[x,y]]
        return np.array([[p.x, p.y] for p in self], dtype="uint32")

    def bounds(self) -> Box:  # return a box that contains all points in self
        return Box(self[0], self[-1])

    # cluster points using DBSCAN algorithm
    def cluster(self, maxd, min_samples=4, n_jobs=-1):
        raw_points = self.as_array()
        db = hdbscan.HDBSCAN(maxd, min_samples, core_dist_n_jobs=n_jobs).fit(raw_points)
        labels = db.labels_
        clusters = []
        max_label = labels.max()
        t1 = time.time()
        for label in range(max_label+1):
            cluster = raw_points[labels == label]
            clusters.append(PointArray.from_array(cluster))
        print('spent {} on converting raw clusters'.format(time.time() - t1))
        return PointArray2D(clusters)

    def middle(self):  # get mean average point
        total = Point(0, 0)
        for p in self:
            total += p
        length = len(self)
        divisor = Point(length, length)
        return total // divisor
