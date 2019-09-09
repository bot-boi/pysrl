from mss.linux import MSS as mss
from threading import Thread, Lock

class Capture:
    def __init__(self, target):
        self.window = target # window to capture
        self.geometry = target.get_geometry()
        self.mut = Lock()    # mutex
        self.thread = Thread(target=self.capture_thread)   # capture thread
        self.kill = False    # used to kill thread
        self.img0 = None   # latest image from thread
        self.img1 = None   # temp img variable

    def start(self):
        self.kill = False
        self.thread = Thread(target = self.ThreadCapture)
        self.thread.start()

    def kill(self):
        self.kill = True

    def capture_thread(self):
        with mss() as sct: # screen capture tool  ?
            while not self.kill:
                raw = self.window.get_image(0, 0, self.geometry.width, self.geometry.height, X.ZPixmap, 0xffffffff)
                rgb = Image.frombytes("RGB", (self.geometry.height,self.geometry.width), raw.data, "raw", "BGRX")
                self.img1 = rgb
                self.mut.acquire()
                self.img0 = self.img1
                self.mut.release()

    def GetImage(self): # gets the latest image
        return self.image0
