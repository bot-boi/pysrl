# color finders and color tolerance speed definitions
import numpy as np
import math
from core.types.point_array import PointArray
from core.types.box import Box

# 3d color range for CTS1 color picking
class RGBCube:
    def __init__(self, color1, color2):
        self.c1 = color1
        self.c2 = color2

    @classmethod # accepts array of CTS1 colors
    def from_colors(class_object, colors):
        res = class_object(CTS1([255,255,255],0), CTS1([0,0,0],0))# result
        for c in colors:
            if c.r > res.c2.r: res.c2.r = c.r
            if c.r < res.c1.r: res.c1.r = c.r
            if c.g > res.c2.g: res.c2.g = c.g
            if c.g < res.c1.g: res.c1.g = c.g
            if c.b > res.c2.b: res.c2.b = c.b
            if c.b < res.c1.b: res.c1.b = c.b
        return res

# TODO: rework color tolerances
# accepts [r,g,b] array and tolerance
# alternate constructor sigs: r, g, b, tol OR color-number, tol
class CTS1:
    def __init__(self, color, tol):
        for i in range(len(color)):
            v = color[i] # value
            if v > 255: color[i]=255
            if v < 0: color[i]=0
        self.color=np.array(color,"uint8")
        self.r = color[0]
        self.b = color[1]
        self.g = color[2]
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

    @classmethod # accepts an array of CTS1 colors & calcs best color -- equiv to BestColor_CTS1
    def from_colors(class_object, colors):
        cube = RGBCube.from_colors(colors)
        r = (cube.c1.r + cube.c2.r) // 2
        g = (cube.c1.g + cube.c2.g) // 2
        b = (cube.c1.b + cube.c2.b) // 2
        tol = math.ceil(math.sqrt((r-cube.c1.r)**2 + (g-cube.c1.g)**2 + (b-cube.c1.b)**2))
        return class_object([r,g,b],tol)

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

