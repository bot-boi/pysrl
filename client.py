# client state evaluation and window interface
from enum import Enum
from ewmh import EWMH
ewmh = EWMH()

from mss.linux import MSS as mss

# get parent of target client window that is also child
# of root window (?).  i dont entirely understand how this works
# but this is how you get a client object with a valid x,y
# offset relative to desktop dimensions

def get_window(title):
    title = title.encode() # needs to be byte
    clients = ewmh.getClientList()
    for client in clients:
        if title in ewmh.getWmName(client):
            return client

def get_frame(client):
    frame = client
    while frame.query_tree().parent != ewmh.root:
        frame = frame.query_tree().parent
    return frame

def get_canvas_recursive(client): # unfinished, cant seem to figure this out reeeee
    canvas_name = "sun-awt-X11-XCanvasPeer".encode()
    result = None
    for child in client.query_tree().children:
        if ewmh.getWmName(child) == canvas_name:
            result = child
            break
        get_canvas_recursive(child)

def get_canvas(client): # search clients children for canvas
    canvas_name = "sun-awt-X11-XCanvasPeer".encode() # TODO: use recursion
    for child in client.query_tree().children:  # tested for runelite only
        for child1 in child.query_tree().children:
            for child2 in child1.query_tree().children:
                if ewmh.getWmName(child2) == canvas_name:
                    return child2

def get_window_frame(title):
    return get_frame(get_window(title))

class CS(Enum): # client state
    LOGGED_IN=0
    LOGIN=1
    WORLD_SWITCHER=2
    LOBBY=3

class Client:
    def __init__(self, window_title):
        self.window_title = window_title
        self.window = get_window(window_title)
        self.canvas = get_canvas(self.window)
        self.frame = get_window_frame(window_title)



