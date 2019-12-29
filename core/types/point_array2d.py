# array of point arrays -- equivalent to SRL's T2DPointArray


# 2dpoint array class -- defines array of array of points and operations upon them
# underlying data is a list in the format [pointarray0,pointarray1,etc]
class PointArray2D(list):
    def filter_size(self, m, M):  # removes clusters outside range min-max -- inplace
        for i, pa in enumerate(self):
            if len(pa) < min or len(pa) > M:
                del self.clusters[i]

    def sort_by_middle(self, middle):  # sort clusters by middle -- inplace
        # sort by distance between midpoint of each point array and middle
        self.sort(key=lambda pa: pa.get_middle().distance_from(middle))
