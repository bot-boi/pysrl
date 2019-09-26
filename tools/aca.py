# auto color aid
# helps pick colors
from Xlib import display, X
from PIL import Image
from pymouse import PyMouseEvent
import numpy as np
import sys

sys.path.append('/home/not-here/Projects/py-srl/')
from core.color import CTS1

def capture_screen():
    dsp = display.Display()
    root = dsp.screen().root
    g = root.get_geometry() # geometry
    raw = root.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xffffffff)
    image = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
    return image

class ACA(PyMouseEvent):
    def __init__(self, mode='CTS1'):
        PyMouseEvent.__init__(self)
        self.mode=mode
        self.colors = []
        self.root = display.Display().screen().root # get root window

    def _capture_screen(self):
        g = self.root.get_geometry()
        raw = self.root.get_image(0, 0, g.width, g.height, X.ZPixmap, 0xffffffff)
        image = Image.frombytes("RGB", (g.width, g.height), raw.data, "raw", "BGRX")
        return image

    def click(self, x, y, button, press):
        if button == 1:
            if press:
                print(np.array(self._capture_screen())[y][x])
        elif button == 2:
            self.stop()
            sys.exit()

if __name__ == "__main__":
    aca = ACA()
    aca.run()

