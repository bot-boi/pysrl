import pyautogui
from core.types.box import Box
from typing import List


def click(offset: (int, int), target: any, button: str):
    # pseudo function overloading
    if type(target) is Box:
        x, y = target.get_point()
        x += offset[0]
        y += offset[1]
    pyautogui.click((x, y), button=button)


def type(keys: str | List[str]):
    # wrapper for when additional functionality is needed
    pyautogui.typewrite(keys)
