import capture as cap
from PIL import Image
import numpy as np

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
