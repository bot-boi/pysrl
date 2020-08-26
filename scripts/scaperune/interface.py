from pysrl.core.types.box import Box
from pysrl.core.types.cts import CTS2
from pysrl.core.types.point import Point
from pysrl.core.client import Client, SR_CANVAS

from pysrl.core.types.image import Image
import pysrl.core.find as find
from typing import List


class Button(Box):
    pass


class Chatbox(Box):
    pass


class Compass(Box):
    def set_north(self):
        pass


class Mainscreen(Box):
    pass


class Minimap(Box):
    @classmethod
    def from_image(obj):
        img = Image.open('./scripts/scaperune/images/fullblah.png')
        border = Image.open('./scripts/scaperune/images/minimap-border.png')
        border.mask = border == [0, 0, 0]
        matches = find.images(img, border)
        for match in matches:
            img = match.draw(img)
        img.show()
    pass


class Slot(Box):
    pass


open_tab_color = CTS2([76, 26, 20], 41, 14, 10)


class InterfaceTab(Box):
    def __init__(self, bounds, btn: Button):
        self.button = btn  # the button that opens the inventory
        p1 = Point(bounds[0], bounds[1])
        p2 = Point(bounds[2], bounds[3])
        super().__init__(p1, p2)

    def isopen(self, img: Image) -> bool:  # check if tab is open
        pts = find.colors(img, open_tab_color, bounds=self.button)
        return len(pts) > 200

    def open(self) -> bool:  # try to open tab, return result
        # not necessary. client.click(this) will work fine i think...
        pass


class Inventory(InterfaceTab):
    def __init__(self, bounds, btn: Button, slots: List[Slot]):
        self.slots = slots
        super().__init__(bounds, btn)

    def debug(self, img: Image):
        img = self.draw(img)
        img = self.button.draw(img)
        for s in self.slots:
            img = s.draw(img)
        img.show()
        return img


# client
client = Client(SR_CANVAS)


# interface buttons
btns = []
btns.append(Button.from_array([522, 195, 555, 227]))  # combat options
btns.append(Button.from_array([564, 195, 589, 227]))  # stats
btns.append(Button.from_array([598, 198, 623, 225]))  # quests
btns.append(Button.from_array([632, 200, 655, 226]))  # inventory
btns.append(Button.from_array([663, 199, 689, 228]))  # equipment
btns.append(Button.from_array([598, 196, 722, 226]))  # prayer
btns.append(Button.from_array([730, 195, 758, 226]))  # magic
btns.append(Button.from_array([527, 495, 559, 523]))  # clan chat
btns.append(Button.from_array([565, 497, 593, 526]))  # friends list
btns.append(Button.from_array([597, 494, 624, 524]))  # ignore list
btns.append(Button.from_array([631, 498, 654, 525]))  # logout
btns.append(Button.from_array([664, 485, 690, 524]))  # options
btns.append(Button.from_array([697, 496, 722, 525]))  # emotes
btns.append(Button.from_array([729, 496, 757, 522]))  # music player


inv_slots = []  # inventory slots
# row 1
inv_slots.append(Slot.from_array([564, 215, 594, 245]))  # slot 0,0
inv_slots.append(Slot.from_array([603, 213, 638, 247]))  # slot 1,0
inv_slots.append(Slot.from_array([645, 212, 681, 249]))
inv_slots.append(Slot.from_array([687, 215, 724, 246]))
# row 2
inv_slots.append(Slot.from_array([565, 249, 595, 282]))
inv_slots.append(Slot.from_array([606, 253, 637, 281]))
inv_slots.append(Slot.from_array([649, 250, 680, 283]))
inv_slots.append(Slot.from_array([690, 248, 722, 283]))
# row 3
inv_slots.append(Slot.from_array([564, 287, 597, 316]))
inv_slots.append(Slot.from_array([605, 285, 636, 318]))
inv_slots.append(Slot.from_array([647, 288, 678, 317]))
inv_slots.append(Slot.from_array([687, 289, 722, 317]))
# row 4
inv_slots.append(Slot.from_array([561, 323, 594, 350]))
inv_slots.append(Slot.from_array([605, 322, 637, 353]))
inv_slots.append(Slot.from_array([647, 323, 678, 351]))
inv_slots.append(Slot.from_array([687, 321, 722, 353]))
# row 5
inv_slots.append(Slot.from_array([563, 359, 594, 390]))
inv_slots.append(Slot.from_array([604, 359, 635, 391]))
inv_slots.append(Slot.from_array([644, 359, 680, 391]))
inv_slots.append(Slot.from_array([688, 361, 720, 389]))
# row 6
inv_slots.append(Slot.from_array([562, 398, 595, 426]))
inv_slots.append(Slot.from_array([606, 397, 635, 424]))
inv_slots.append(Slot.from_array([644, 394, 680, 426]))
inv_slots.append(Slot.from_array([687, 396, 723, 426]))
# row 7
inv_slots.append(Slot.from_array([561, 429, 597, 462]))
inv_slots.append(Slot.from_array([605, 431, 638, 459]))
inv_slots.append(Slot.from_array([646, 433, 680, 460]))
inv_slots.append(Slot.from_array([690, 431, 722, 460]))


interface_tabs_boxr = [552, 205, 733, 464]  # interface tab box raw
inv_button = Button.from_array([628, 170, 658, 201])
inventory = Inventory(interface_tabs_boxr, inv_button, inv_slots)


chatbox = Chatbox.from_array([4, 368, 517, 503])
compass = Compass.from_array([536, 0, 584, 43])
mainscreen = Box.from_array([4, 4, 516, 338])
# minimap = Minimap(Point(644, 84), 74)
