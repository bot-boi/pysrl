import math
import random
from .point import Point


class Circle:
    def __init__(self, center: Point, radius: int):
        self.center = center
        self.radius = radius

    def __contains__(self, other: Point):
        c = self.center
        p = other
        d = math.sqrt((p.x - c.x) + (p.y - c.y))
        return d < self.radius

    # get a random point in self
    def get_point(self) -> Point:
        angle = 2 * math.pi * random.random()
        r = self.radius * math.sqrt(random.random())
        x = r * math.cos(angle) + self.center.x
        y = r * math.cos(angle) + self.center.y
        return Point(x, y)
