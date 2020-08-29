import math
import numpy as np
import random
from .box import Box
from .image import Image
from .point import Point
from .point_array import PointArray


class Circle:
    def __init__(self, center: Point, radius: int):
        self.center = center
        self.radius = radius

    def __contains__(self, other: Point):
        c = self.center
        p = other
        d = math.sqrt((p.x - c.x) + (p.y - c.y))
        return d < self.radius

    def get_box(self) -> Box:  # get a box that contains self
        top_left = self.center
        top_left.x -= self.radius
        top_left.y -= self.radius
        bot_right = self.center
        bot_right.x += self.radius
        bot_right.y += self.radius
        return Box(top_left, bot_right)

    # get the chunk of img that fits in self
    def get_image_slice(self, img: Image, mask_color=[255, 0, 0]):
        # the obvious solution
        img = img.copy()
        # make box around self
        bounds = self.get_box()
        img = img[bounds.y0: bounds.y1, bounds.x0: bounds.x1]
        # iterate all possible points in the box
        ys = range(0, bounds.height)
        xs = range(0, bounds.width)
        mask = np.full((bounds.height, bounds.width), False)
        # if point is not in circle, mask it or draw over it
        for y in ys:
            for x in xs:
                mask[y, x] = (Point(x, y) not in self)
        if mask_color is None:
            # hav 2 invert for the actual .mask attribute
            img.mask = ~mask
            return img
        else:
            img[mask] = mask_color
            return img

    # get list of points at edge of circle
    def get_edges(self) -> PointArray:
        x = self.center.x
        y = self.center.y
        r = self.radius
        xs = []  # x's
        ys = []  # y's
        for angle in range(0, 360 + 1):
            xs.append(int(x + r * math.cos(angle * (math.pi / 180))))
            ys.append(int(y + r * math.sin(angle * (math.pi / 180))))
        raw = np.stack((xs, ys), axis=1)
        raw = np.unique(raw, axis=1)
        return raw.view(PointArray)

    # get a random point in self
    def get_point(self) -> Point:
        angle = 2 * math.pi * random.random()
        r = self.radius * math.sqrt(random.random())
        x = r * math.cos(angle) + self.center.x
        y = r * math.cos(angle) + self.center.y
        return Point(x, y)

    def draw(self, img: Image, color=[255, 0, 0]) -> Image:
        img = img.copy()
        edge = self.get_edges()  # x, y 
        for p in edge:
            img[p[0], p[1]] = color
        return img
