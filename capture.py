from threading import Thread, Lock
from PIL import Image
from Xlib import X, error as Xerror
from conversions import rgb_to_hsl
from copy import deepcopy
from client import get_window, get_canvas

# Capture class, represents constant capture of a window
# init with Capture(ClientWindow("RuneLite"))
class Capture:
    def __init__(self, window_title):
        self.window = get_window(window_title)
        self.target = get_canvas(self.window)
        self.mut = Lock()     # mutex TODO: rename to lock with fancy search replace vim functionality
        self.thread = None    # the capture thread (init w/ self.start())
        self.kill = False     # used to kill thread capture thread
        self.img_rgb = None   # rgb version of img
        self.img_hsl = None   # hsl version of img

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
            if self.kill: # check if killed
                return 0
            # get the shape of the window and reload canvas if it fails
            try:
                g = self.target.get_geometry()
            except Xerror.BadDrawable:
                self.target = get_canvas(self.window)
                g = self.target.get_geometry()
            # get raw img data of window NOTE: these are python xlib calls
            raw = self.target.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xffffffff)
            # convert raw to RGB Pillow Image
            rgb = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
            # convert RGB image to HSL
            # hsl = rgb_to_hsl(rgb)
            # output the rgb and hsl images for use
            self.mut.acquire()
            self.img_rgb = rgb
            # self.img_hsl = hsl
            self.mut.release()

    # returns latest capture  in rgb and hsl format
    def get_image(self):
        self.mut.acquire()                 # TODO: figure out if copy is needed
        temp_rgb = self.img_rgb # is deep copy necessary? i think it is, since self.img_rgb &
        temp_hsl = self.img_hsl # self.img_hsl are being accessed by another thread constantly
        self.mut.release()
        return temp_rgb, temp_hsl
