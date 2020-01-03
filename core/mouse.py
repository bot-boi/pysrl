from enum import Enum

# mouse button
class Mbtn(Enum):
    RIGHT = 0
    LEFT = 1
    MIDDLE = 2
    MOVE = 3

# moves mouse to x,y coords
def _movemouse(x, y):

# moves mouse to x,y coords and presses mbtn
def movemouse(x, y, mbtn):
