# non-rotateable bounding box
from core.types.point import Point
import numpy as np


class Box:
    # accepts 2 Points
    def __init__(self, top_left: Point, bot_right: Point):
        # type: (Point, Point) -> None
        self.top_left = top_left  # top left corner
        self.bot_right = bot_right  # bot right corner
        self.x1 = top_left.x
        self.y1 = top_left.y
        self.x2 = bot_right.x
        self.y2 = bot_right.y
        self.width = self.x2-self.x1
        self.height = self.y2-self.y1

    def __str__(self) -> str:
        return "Box([{}, {}], [{}, {}])".format(self.x1, self.y1, self.x2, self.y2)

    @classmethod  # accepts [x1, y1, x2, y2]
    def from_array(class_object, arr):
        if len(arr) == 4:
            return class_object(Point.from_array(arr[:2]), Point.from_array(arr[2:]))
        else:
            raise ValueError("Passed array with length {}, needs to be length 4".format(len(arr)))

    # return a point array of points contained within box
    def contains(self, points):
        return np.array([p for p in points
                         if p[0] >= self.x1 and p[0] <= self.x2
                         and p[1] >= self.y1 and p[1] <= self.y2])

    # draw box on image
    def draw(self, img, color=np.array([255, 0, 0])):
        def draw_line(img, start, axis, length, color=np.array([255, 0, 0])):
            if axis == 'x':
                y = start.y
                for x in range(start.x, start.x + length):
                    img[y][x] = color
            elif axis == 'y':
                x = start.x
                for y in range(start.y, start.y + length):
                    img[y][x] = color
        draw_line(img, self.top_left,  'x', self.width)
        draw_line(img, self.top_left,  'y', self.height)
        top_right = self.top_left + Point(self.width, 0)
        bot_left = self.top_left + Point(0, self.height)
        draw_line(img, top_right, 'y', self.height)
        draw_line(img, bot_left, 'x', self.width)
        return img
