# non-rotateable bounding box
from pysrl.core.types.point import Point
import pysrl.core.draw as draw
import itertools
import numpy as np
import random


class Box:
    """
    Representation of a perfectly square box.

    ...
    Attributes
    ----------
        top_left : Point
            top left corner of the box
        bot_right : Point
            bottom right corner of the box
        x0, y0 : int
            top left split by dimension
        x1, y1 : int
            bottom right split by dimension
        width : int
            the width of the box
        height : the height of the box

    Methods
    -------
        from_array -> Box
            instantiate a Box from an array ie. [0, 0, 9, 9]
        contains(points:) -> List[Point]:
            returns all elements in points contained in the box
        draw(img: np.ndarray, color: List[int]) -> np.ndarray:
            returns an image with this box drawn on it
        get_point() -> (int, int)
            returns a random point in Self
    """
    def __init__(self, top_left: Point, bot_right: Point):
        # type: (Point, Point) -> None
        self.top_left = top_left  # top left corner
        self.bot_right = bot_right  # bot right corner
        self.x0 = top_left.x
        self.y0 = top_left.y
        self.x1 = bot_right.x
        self.y1 = bot_right.y
        self.width = self.x1-self.x0
        self.height = self.y1-self.y0

    def __str__(self) -> str:
        return "Box([{}, {}], [{}, {}])".format(self.x0, self.y0, self.x1, self.y1)

    @classmethod
    def from_array(class_object, arr):
        """
        Creates a Box from an array with shape [x0, y0, x1, y1]
        """
        if len(arr) == 4:
            return class_object(Point.from_array(arr[:2]), Point.from_array(arr[2:]))
        else:
            raise ValueError("Passed array with length {}, needs to be length 4".format(len(arr)))

    def contains(self, points):
        """
        Returns all points contained within self.

        Parameters
        ----------
            points: the points that may or may not be contained in self

        Returns
        -------
            all points contained within self

        """
        return np.array([p for p in points
                         if p[0] >= self.x0 and p[0] <= self.x1
                         and p[1] >= self.y0 and p[1] <= self.y1])

    def get_point(self) -> (int, int):
        x = random.randrange(self.x0, self.x1)
        y = random.randrange(self.y0, self.y1)
        return (x, y)

    def draw(self, img: np.ndarray, color=[255, 0, 0]):
        """
        Draws a box on an image.

        Parameters
        ----------
            img: the image (in numpy form) to be drawn upon
            color: the color the line should be (default=red)

        Returns
        -------
            img: the image (in numpy form) that has been drawn upon

        """
        if len(color) != 3:
            raise Exception("invalid color passed to core.types.box.draw")
        color = np.array(color)
        l0 = draw.line(self.x0, self.y0, self.x1, self.y0)
        l1 = draw.line(self.x0, self.y0, self.x0, self.y1)
        l2 = draw.line(self.x1, self.y1, self.x1, self.y0)
        l3 = draw.line(self.x1, self.y1, self.x0, self.y1)
        square = itertools.chain(l0, l1, l2, l3)
        for x, y in square:
            img[x][y] = color

        return img
