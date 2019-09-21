import capture as cap
from PIL import Image
import numpy as np
import math

# cp = cap.Capture("RuneLite")
# cp.start()

test_img = Image.open("test.jpeg")

class Box:
    def __init__(self, x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.width=x2-x1
        self.height=y2-y1

# accepts [r,g,b] array and tolerance
# alternate constructor sigs: r, g, b, tol OR color-number, tol
class CTS1:
    def __init__(self, color, tol):
        for i in range(len(color)):
            v = color[i] # value
            if v > 255: color[i]=255
            if v < 0: color[i]=0
        self.color=np.array(color,"uint8")
        self.tol=tol
        m = [] # min
        M = [] # max
        # handle overflow/underflow
        for i in range(len(self.color)): # there has to be a more elegant way to do this
            v = self.color[i]
            if v+tol > 255:
                M.append(255)
            else:
                M.append(v+tol)
            if v-tol < 0:
                m.append(0)
            else:
                m.append(v-tol)
        self.min = np.array(m, "uint8")
        self.max = np.array(M, "uint8")

def distance_between(a,b):
    print(a,b)
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
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

    def cluster(self, max_dist): # naive clustering algorithm
        unclustered = self.points.copy()
        clusters = []        # 2DPointArray -- array of point arrays
        c_cluster = 0  # current cluster
        while len(unclustered) > 0:
            cs = unclustered[0]        # cluster start -- 1st point in a new cluster
            cluster = PointArray([cs]) # the cluster being found
            unclustered = np.delete(unclustered, 0, 0) # delete cs from unclustered
            print(len(unclustered))
            clustered_indices = [] # indices of points in unclustered that've been clustered
            for i,candidate in enumerate(unclustered):
                for clustered_point in cluster.points:
                    if distance_between(candidate, clustered_point) <= max_dist:
                        cluster.append(candidate)
                        # unclustered = np.delete(unclustered, i, 0)
                        clustered_indices.append(i)
                        break # no need to keep checking

            unclustered = np.delete(unclustered, clustered_indices, 0)
            clusters.append(cluster)

        return clusters

# returns points of an image that're within color +/- tolerance & bounds
# color is the CTS1 class
def find_colors(img, color, bounds=None):
    arr = np.array(img)
    if bounds == None:
        bounds = Box(0,0,img.width,img.height)
    b = bounds
    arr = arr[b.y1:b.y2, b.x1:b.x2] # apply bounds
    x,y = np.where(np.all(np.logical_and(np.less_equal(arr,color.max), np.greater_equal(arr,color.min)), 2))
    points = np.column_stack((x,y))
    return points

# draw point array
def draw_pa(img, pa, color=np.array([255,0,0],dtype="uint8")):
    data = np.array(img)
    for p in pa:
        data[p[0],p[1]] = color
    return Image.fromarray(data)

def filter_near(a,b,dist):
    '''returns all points in a within some distance to a point in b'''
    if len(a) == 0 or len(b) == 0:
        return np.asarray([])
    diffs = np.asarray([(i,np.min(np.sum(np.square(p-b),axis=-1))) for i,p in enumerate(a)])
    return a[diffs[:,1]<dist*dist]

color = CTS1([50, 150, 50], 50)
points = find_colors(test_img, color)
draw_pa(test_img,points).show()
pa = PointArray(points)
clusters = pa.cluster(5)

img = test_img.copy()
for c in clusters:
    img = draw_pa(img, c, np.random.randint(255,size=3,dtype="uint8"))

img.show()
