# client state evaluation and window interface
from enum import Enum

class CS(Enum):
    LOGGED_IN=0
    LOGIN=1
    WORLD_SWITCHER=2
    LOBBY=3
