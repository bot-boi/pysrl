import capture as cap
from PIL import Image
import numpy as np

cp = cap.Capture("RuneLite")
cp.start()

test_img = Image.open("test.jpeg")

class Box:
    def __init__(self, x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.width=x2-x1
        self.height=y2-y1

# returns points of an image that're within color +/- tolerance & bounds
# color is a 3 element numpy array
def find_colors(img, color, tolerance=0, bounds=Box(0,0,img.width,img.height)):
    arr = np.array(img)
    bounds = b
    arr = arr[b.y1:b.y2, b.x1:b.x2] # apply bounds
    arr = arr[(arr > color + tolerance) and (arr < color - tolerance)] = 0
    points = arr.where((arr > color + tolerance) and (arr < color - tolerance)) # create the mask
    mask = mask.astype(np.int)
    colors = mask * arr # apply the mask
    points = np.where(mask == 1)
