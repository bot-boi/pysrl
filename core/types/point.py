# representation of a 2d point
import math


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod  # accepts list or numpy array with format [x,y]
    def from_array(class_object, arr):
        return class_object(arr[0], arr[1])

    def __add__(self, other):
        return Point(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        return Point(self.x*other.x, self.y*other.y)

    def __floordiv__(self, other):
        return Point(self.x // other.x, self.y // other.y)

    def distance_from(self, other):  # get distance from another point
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
