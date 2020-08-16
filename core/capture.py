from Xlib import X, error as Xerror
from pysrl.core.types.image import Image
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
            bools.append(self.id == other.id)
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
SIMP_WINDOW = XObjPattern(name="Simplicity RSPS - The Biggest \
                                Pre-EOC Server 2020")
SIMP_CANVAS = XObjPattern(name="sun-awt-X11-XPanelPeer")


def findxwindow(pattern: XObjPattern):
    """
    Finds an XWindow object recursively.

    Parameters
    -----------
        pattern - pattern describing the desired XWindow object

    Returns
    -------
        matches - list of xwindow objects that match the pattern
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


def get_frame(window):
    # get window manager frame of window
    while window.query_tree().parent.id != ewmh.root.id:
        window = window.query_tree().parent
    return window


def get_offset(window) -> (int, int):
    # get x,y offset of a window relative to root
    xoff = 0
    yoff = 0
    while window.id != ewmh.root.id:
        g = window.get_geometry()
        xoff += g.x
        yoff += g.y
        window = window.query_tree().parent
    return (xoff, yoff)


class Capture:  #
    def __init__(self, canvas_pattern: XObjPattern):
        # get canvas and its frame and offset relative to root coords
        self.canvas_pattern = canvas_pattern
        self.canvas = findxwindow(self.canvas_pattern)[0]
        self.frame = get_frame(self.canvas)
        self.offset = get_offset(self.canvas)

    def get_image(self) -> Image:
        # get the shape of the window and reload canvas if it fails
        # canvas id changes on resize, other events cause this too ?
        try:
            g = self.canvas.get_geometry()
        except Xerror.BadDrawable or Xerror.BadMatch:
            print("bad drawable")
            self.canvas = findxwindow(self.canvas_pattern)[0]
            g = self.canvas.get_geometry()
        raw = self.canvas.get_image(0, 0, g.width, g.height, X.ZPixmap,
                                    0xffffffff)
        if type(raw.data) is str:
            # case: window covered
            # TODO: handle minimized window?
            ewmh.setActiveWindow(self.frame)
            ewmh.display.flush()  # force targeted window to top
            raw = self.canvas.get_image(0, 0, g.width, g.height, X.ZPixmap,
                                        0xffffffff)
        img = Image.frombytes((g.width, g.height), raw.data)
        return img
