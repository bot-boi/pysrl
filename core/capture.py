from threading import Thread, Lock
from PIL import Image
from Xlib import X, error as Xerror
import time
import numpy as np
from ewmh import EWMH
ewmh = EWMH()


class XObjPattern:
    """
    Pattern class, used to find XWindow objects

    ...
    Attributes
    ----------
        id : int
            find by XWindow ID
        name : str
            find by XWindow name

    Methods
    -------
    match(other) -> bool:
        returns true if pattern matches
    """
    def __init__(self, ID=None, name=None):
        """
        Parameters
        ----------
            ID : int
                find by XWindow ID
            name : str
                find by XWindow name

        parameters not supplied will be ignored in match
        """
        self.id = ID
        self.name = name

    def match(self, other) -> bool:
        """
        Checks if pattern and XWindow object match

        ...
        Parameters
        ----------
            other : Xlib.display.Window
                the object to be matched

        Returns
        -------
            bool
        """
        bools = []
        if self.id:
            bools.append(self.id == ewmh.getWmPid(other))
        if self.name:
            othername = ewmh.getWmName(other)
            if type(othername) == bytes:  # sometimes wm names are bytes
                othername = othername.decode()  # other times they are str?
            bools.append(self.name == othername)
        for b in bools:
            if b is False:
                return False
        return True


RL_WINDOW = XObjPattern(name="RuneLite")
RL_CANVAS = XObjPattern(name="sun-awt-X11-XCanvasPeer")
SIMP_WINDOW = XObjPattern(name="Simplicity RSPS - The Biggest Pre-EOC Server 2020")
SIMP_CANVAS = XObjPattern(name="sun-awt-X11-XPanelPeer")


def findxobj(pattern: XObjPattern):
    """
    Finds an XWindow object recursively.

    Parameters
    -----------
        pattern : XObjPattern
            pattern describing the desired XWindow object

    Returns
    -------
        matches : List[Xlib.display.Window]
            list of xwindow objects that match the pattern
    """
    matches = []

    def recursion(obj):
        if obj is None:
            return
        if pattern.match(obj):
            matches.append(obj)
        if obj.query_tree().children:
            for i in obj.query_tree().children:
                recursion(i)

    recursion(ewmh.root)
    return matches


# Capture class, represents constant capture of a window
# init with Capture(ClientWindow("RuneLite"))
class Capture:
    def __init__(self, windowpattern, canvaspattern):
        self.windowpattern = windowpattern
        self.canvaspattern = canvaspattern
        self.window = findxobj(windowpattern)[0]  # TODO: handle case no object and case multiple same object?
        self.target = findxobj(canvaspattern)[0]  # where we grab img from
        self.lock: Lock = Lock()    # mutex lock thing
        self.thread: Thread = None  # the capture thread (init w/ self.start())
        self.kill: bool = False     # used to kill thread capture thread
        self.image: Image = None

    # starts the capture thread
    def start(self):
        self.kill = False
        self.thread = Thread(target=self.capture_thread)
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
            if self.kill:  # check if killed
                return 0

            # get the shape of the window and reload canvas if it fails
            # canvas id changes on resize, other events cause this too ?
            try:
                g = self.target.get_geometry()
            except Xerror.BadDrawable or Xerror.BadMatch:
                print("bad drawable")
                self.target = findxobj(self.canvaspattern)
                g = self.target.get_geometry()
            # get raw img data of window NOTE: these are python xlib calls
            raw = self.target.get_image(0, 0, g.width, g.height, X.ZPixmap,
                                        0xffffffff)
            # convert raw to opencv image
            if type(raw.data) == str:
                # this means window is minimized or covered (not rendering)
                print('Window hidden, slowing capture to every 10 seconds',
                      flush=True)
                time.sleep(10)
            else:
                img = Image.frombytes("RGB", (g.width, g.height), raw.data,
                                      "raw", "BGRX")
                if img is None:
                    print('img grab failed')
                # output image
                self.lock.acquire()
                self.image = np.array(img.copy())
                self.lock.release()
                # t2 = time.time()
                # print("capture thread ran in {}".format(t2-t1))

    # returns latest capture
    def get_image(self) -> np.ndarray:
        self.lock.acquire()
        arr = np.copy(self.image)
        self.lock.release()
        print(arr)
        return arr
