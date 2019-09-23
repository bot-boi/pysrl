# color finders and color tolerance speed definitions
import numpy as np
from core.types.point_array import PointArray
from core.types.box import Box

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


# returns points of a PIL Image that're within color +/- tolerance & bounds
# color is the CTS1 class
def find_colors(img, color, bounds=None):
    arr = np.array(img)
    if bounds == None:
        bounds = Box.from_array([0,0,img.width,img.height])
    b = bounds
    arr = arr[b.y1:b.y2, b.x1:b.x2] # apply bounds
    x,y = np.where(np.all(np.logical_and(np.less_equal(arr,color.max), np.greater_equal(arr,color.min)), 2))
    points = np.column_stack((x,y))
    return PointArray.from_array(points)

