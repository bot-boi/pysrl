import time
import os
from pysrl.core.client import Client, SR_CANVAS
import pysrl.core.find as find


class SRClient(Client):
    def __init__(self):
        super().__init__(SR_CANVAS)


client = SRClient()


def rest():
    time.sleep(0.5)


def login(username, password) -> bool:
    # press 'Existing User' button
    img = client.get_image()
    step1 = find.text(img, 'Existing User')
    client.click(step1, button='left')
    rest()
    client.type(username)
    rest()
    client.type(['enter'])
    rest()
    client.type(password)
    rest()
    client.type(['enter'])
    time.sleep(3)
    img2 = client.get_image()
    step2 = find.text(img2, 'CLICK HERE TO PLAY')
    client.click(step2)
    rest()
    # return IsLogin()
    return True  # need to check if login was succesful


username = os.environ['SCAPERUNE_USERNAME']
password = os.environ['SCAPERUNE_PASSWORD']
login('bananajones', 'thisisbananajones')
