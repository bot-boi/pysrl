# array of point arrays -- equivalent to SRL's T2DPointArray


# 2dpoint array class, defines array of array of points and operations on them
# underlying data is a list in the format [pointarray0,pointarray1,etc]
def filtersize(arr, m, M):  # removes clusters outside range m/M
    return [pts for pts in arr if len(pts) > m and len(pts) < M]


def sort_by_middle(self, middle):  # sort clusters by middle -- inplace
    # sort by distance between midpoint of each point array and middle
    self.sort(key=lambda pa: pa.middle().distance_from(middle))
