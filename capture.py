from threading import Thread, Lock
from PIL import Image
from Xlib import X, error as Xerror
from conversions import rgb_to_hsl
from copy import deepcopy
from client import get_window, get_canvas
from enum import Enum
from ewmh import EWMH
ewmh = EWMH()
import time

# stuff for getting client xwindow
# get xwindow object
def get_window(title):
    title = title.encode() # needs to be byte
    clients = ewmh.getClientList()
    for client in clients:
        if title in ewmh.getWmName(client):
            return client

# get frame of an xwindow object
# works for runelite, unsure for other apps
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

# get runelite canvas
def get_canvas(client): # search osrs client children for canvas
    canvas_name = "sun-awt-X11-XCanvasPeer".encode() # TODO: use recursion
    for child in client.query_tree().children:  # tested for runelite only
        for child1 in child.query_tree().children:
            for child2 in child1.query_tree().children:
                if ewmh.getWmName(child2) == canvas_name:
                    return child2

# get frame of an xwindow, accepts name of window
def get_window_frame(title):
    return get_frame(get_window(title))

# Capture class, represents constant capture of a window
# init with Capture(ClientWindow("RuneLite"))
class Capture:
    def __init__(self, window_title):
        self.window = get_window(window_title)
        self.target = get_canvas(self.window)
        self.lock = Lock()    # mutex lock thing
        self.thread = None    # the capture thread (init w/ self.start())
        self.kill = False     # used to kill thread capture thread
        self.image = None     # PIL Image

    # starts the capture thread
    def start(self):
        self.kill = False
        self.thread = Thread(target = self.capture_thread)
        self.thread.start()

    # terminates the capture thread
    def terminate(self):
        self.kill = True

    # thread capture job
    # TODO: it might make more sense to output arrays of pixels
    # instead of Image objects
    def capture_thread(self):
        while True:
            # t1 = time.time()
            if self.kill: # check if killed
                return 0

            # get the shape of the window and reload canvas if it fails
            # canvas id changes on resize, other events cause this too ?
            try:
                g = self.target.get_geometry()
            except Xerror.BadDrawable:
                self.target = get_canvas(self.window)
                g = self.target.get_geometry()
            # get raw img data of window NOTE: these are python xlib calls
            raw = self.target.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xffffffff)
            # convert raw to RGB Pillow Image
            rgb = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
            # output image
            self.lock.acquire()
            self.image = rgb
            self.lock.release()
            # t2 = time.time()
            print("capture thread ran in {}".format(t2-t1))

    # returns latest capture
    def get_image(self):
        self.lock.acquire()
        img = self.image    # is a deep copy necessary?
        self.lock.release()
        return img
