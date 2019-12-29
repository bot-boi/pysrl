# auto color aid
# helps pick colors
from Xlib import display, X
from PIL import Image
from pymouse import PyMouseEvent
import numpy as np
import sys
from core.color import find_colors
from core.types.cts import CTS1, CTS2
from core.debug import draw_pa2d
sys.path.append('/home/not-here/Projects/py-srl/')


def capture_screen():
    dsp = display.Display()
    root = dsp.screen().root
    g = root.get_geometry()  # geometry
    raw = root.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
    return image


class _MouseHandler(PyMouseEvent):
    events = []

    def __init__(self):
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        self.events.append((x, y, button, press))


class ListenInterrupt(Exception):
    pass


class ACA(PyMouseEvent):
    def __init__(self, mode='CTS2'):
        PyMouseEvent.__init__(self)
        self.quit = False
        self.mode = mode
        self.colors = []
        self.root = display.Display().screen().root  # get root window

    def _capture_screen(self):
        g = self.root.get_geometry()
        raw = self.root.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xffffffff)
        image = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
        return image

    def _get_user_input(self):
        cmd = input("What would you like to do?\n")
        if cmd == "help":
            print("select-color or sc, undo or u, clear or c, mode or m, result or r, show or s, quit or q, help")
        elif cmd == "select-color" or cmd == "sc":
            print("use right click to exit")
            try:
                self.run()
            except ListenInterrupt as e:
                print(e.args[0])
        elif cmd == "undo" or cmd == "u":
            # removes last color added
            del self.colors[-1]
        elif cmd == "clear" or cmd == "c":
            self.colors = []
        elif cmd == "mode" or cmd == "m":
            self.mode = input("Enter mode (CTS1, CTS2)")
        elif cmd == "result" or cmd == "r":
            res = None
            if self.mode == "CTS1":
                res = CTS1.from_colors(self.colors)
                print(res.color, res.tol)
            elif self.mode == "CTS2":
                res = CTS2.from_colors(self.colors)
                print(res.color, res.rtol, res.btol, res.gtol)
        elif cmd == "show" or cmd == "s":
            color = None
            if self.mode == "CTS1":
                color = CTS1.from_colors(self.colors)
            elif self.mode == "CTS2":
                color = CTS2.from_colors(self.colors)
            img = self._capture_screen()
            pa = find_colors(img, color)
            draw_pa2d(img, pa.cluster(5)).show()
        elif cmd == "quit" or cmd == "q":
            self.quit = True

    def my_run(self):  # run is already defined in PyMouseEvent
        # TODO: have separate class for mouse events
        while not self.quit:
            self._get_user_input()
        sys.exit()

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                rgb = np.array(self._capture_screen(), dtype="uint64")[y][x]
                print(rgb)
                self.colors.append(CTS1(rgb, 0))
        elif button == 2:
            raise ListenInterrupt("Exiting click mode")


if __name__ == "__main__":
    aca = ACA()
    aca.my_run()
