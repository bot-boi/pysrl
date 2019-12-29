# array of points -- equivalent to SRL's TPointArray
import numpy as np
from sklearn.cluster import DBSCAN
from core.types.point_array2d import PointArray2D
from core.types.point import Point


# point array class -- defines array of points and operations upon them
# underlying data is an array of Point
class PointArray(list):

    @classmethod  # alternate constructor -- accepts numpy array w/format [[x,y]]
    def from_array(class_object, arr):
        points = []
        for p in arr:
            points.append(Point.from_array(p))
        return class_object(points)

    def as_array(self):  # returns points as numpy array -- [[x,y]]
        return np.array([[p.x, p.y] for p in self], dtype="uint32")

    def cluster(self, max_dist, min_samples=4, n_jobs=8):  # cluster points using DBSCAN algorithm
        raw_points = self.as_array()
        db = DBSCAN(max_dist, min_samples, n_jobs=n_jobs).fit(raw_points)
        labels = db.labels_
        clusters = []
        max_label = labels.max()
        for label in range(max_label+1):
            cluster = raw_points[labels == label]
            clusters.append(PointArray.from_array(cluster))
        return PointArray2D(clusters)

    def get_middle(self):  # get mean average point
        total = Point(0, 0)
        for p in self:
            total += p
        length = len(self)
        divisor = Point(length, length)
        return total // divisor
