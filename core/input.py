import pyautogui
from pysrl.core.types.box import Box
from pysrl.core.types.point import Point


def click(offset: (int, int), target: any, button: str):
    # pseudo function overloading
    x = target.x
    y = target.y
    x += offset[0]
    y += offset[1]
    pyautogui.click((x, y), button=button)


def type(keys):  # keys can be str or List[str]
    # wrapper for when additional functionality is needed
    pyautogui.typewrite(keys)
