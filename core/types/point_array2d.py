# array of point arrays -- equivalent to SRL's T2DPointArray
import numpy as np

# 2dpoint array class -- defines array of array of points and operations upon them
# underlying data is a list in the format [pointarray0,pointarray1,etc]
class PointArray2D():
    def __init__(self, clusters):
        self.clusters = clusters

    def __delitem__(self, key): # allow indexing like an array
        del self.clusters[key]

    def __getitem__(self, key):  # allow indexing like an array
        return self.clusters[key]

    def __setitem__(self, key, value): # allow indexing like an array
        self.clusters[key] = value

    def __len__(self):
        return len(self.clusters)

    def append(self, point_array): # appends a cluster (point array) to self.clusters
        self.clusters.append(point_array)

    def filter_size(self, m, M): # removes clusters outside range min-max -- inplace
        for i, pa in enumerate(self.clusters):
            if len(pa) < min or len(pa) > M:
                del self.clusters[i]

    # def sort_by_middle(self, middle): # sort clusters by middle -- inplace



