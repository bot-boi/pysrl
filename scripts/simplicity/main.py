# pysrl needs be in PYTHONPATH for this to work
import numpy as np
import os
from PIL import Image
from pysrl.core.capture import Capture, SIMP_CANVAS, get_offset
from pysrl.core.types.point import Point
import pysrl.core.input as inp  # input is reserved...


cp = Capture(SIMP_CANVAS)

username_needle = np.array(Image.open('./username.png').convert('RGB'))
password_needle = np.array(Image.open('./password.png').convert('RGB'))
offset = (0, 15)  # offset from user/pass loc so we can click the input box


# NOTE: images to be found have to be screenshot of Image.show
def login(username: str, password: str):
    img = cp.get_image()
    userloc = Point(282, 163)
    yoffset = 25
    userloc.y += yoffset
    img = userloc.draw(img)
    # Image.fromarray(img).show()
    inp.click(get_offset(cp.canvas), userloc, 'left')
    inp.type(username)
    inp.type(['enter'])
    inp.type(password)
    inp.type(['enter'])


username = os.environ['SIMP_USER']
password = os.environ['SIMP_PASS']
login(username, password)
