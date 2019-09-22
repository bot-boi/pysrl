import capture as cap
from PIL import Image
import numpy as np
import math
from sklearn.cluster import DBSCAN

from core.color import CTS1, find_colors
from core.debug import draw_pa
from core.types.point_array import PointArray
import time

# cp = cap.Capture("RuneLite")
# cp.start()

test_img = Image.open("test.jpeg")
color = CTS1([10, 30, 70], 50)
pa = find_colors(test_img, color)
draw_pa(test_img,pa).show()

t1 = time.time()
clusters = pa.cluster(2)
print("clustered in", time.time()-t1)

img = test_img.copy()
for c in clusters:
    img = draw_pa(img, PointArray(c), np.random.randint(255,size=3,dtype="uint8"))
img.show()
