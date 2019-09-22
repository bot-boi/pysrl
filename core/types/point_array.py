# array of points -- equivalent to SRL's TPointArray
import numpy as np
from sklearn.cluster import DBSCAN

# point array class -- defines array of points and operations upon them
# underlying data is a 2d numpy array in the format [[x0,y0],[x1,y1],etc]
class PointArray():
    def __init__(self, points):
        self.points = points

    def __delitem__(self, key): # allow indexing like an array
        del self.points[key]

    def __getitem__(self, key):  # allow indexing like an array
        return self.points[key]

    def __setitem__(self, key, value): # allow indexing like an array
        self.points[key] = value

    def append(self, point): # appends a point [x,y] to self.points
        self.points = np.vstack((self.points, point))

    def cluster(self, max_dist, min_samples=4, n_jobs=8): # cluster points using DBSCAN algorithm
        db = DBSCAN(max_dist, min_samples, n_jobs=n_jobs).fit(self.points)
        labels = db.labels_
        clusters = []
        max_label = labels.max()
        for label in range(max_label+1):
            cluster = self.points[labels == label]
            clusters.append(cluster)
        return clusters # TODO: this should return 2DPointArray type, not raw numpy array
