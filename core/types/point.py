# representation of a 2d point
import math
import numpy as np
import pysrl.core.draw as draw


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod  # accepts list or numpy array with format [x,y]
    def from_array(class_object, arr):
        return class_object(arr[0], arr[1])

    def __eq__(self, other) -> bool:
        return (self.x == other.x and self.y == other.y)

    def __str__(self) -> str:
        return "Point({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y)

    def __floordiv__(self, other):
        return Point(self.x // other.x, self.y // other.y)

    def distance_from(self, other):  # get distance from another point
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def draw(self, img: np.ndarray, color=(255, 0, 0), size=10):
        # avoid circular input with box
        from pysrl.core.types.box import Box
        if len(color) != 3:
            raise Exception('Invalid color passed to Point.draw')
        # get a square around self, draw line from self to sqr's corners
        xb, yb, _ = img.shape  # x bounds, y bounds
        off = size  # axis offset
        x = self.x
        y = self.y  # handle out of bounds cases
        mx = x - off if x >= off else 0
        my = y - off if y >= off else 0
        Mx = x + off if x + off <= xb else xb
        My = y + off if x + off <= yb else yb
        square = Box.from_array([mx, my, Mx, My])
        line1 = draw.line(square.x0, square.y0, square.x1, square.y1)
        line2 = draw.line(square.x1, square.y0, square.x0, square.y1)
        for p in line1:
            img[p[1], p[0]] = color
        for p in line2:
            img[p[1], p[0]] = color
        return img
