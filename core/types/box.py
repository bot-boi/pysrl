# non-rotateable bounding box
from core.types.point import Point
from typing import List


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

    @classmethod  # accepts [x1, y1, x2, y2]
    def from_array(class_object, arr: List[int]):
        if len(arr) == 4:
            return class_object(Point.from_array(arr[:2]), Point.from_array(arr[2:4]))
        else:
            raise ValueError("Passed array with length {}, needs to be length 4".format(len(arr)))
