# color tolerance speed types
# color finders and color tolerance speed definitions
import numpy as np
import math
from typing import List


# 3d color range for CTS1 color picking
class RGBCube:
    def __init__(self, color1, color2):
        self.c1 = color1
        self.c2 = color2

    @classmethod  # accepts array of CTS1 colors
    def from_colors(class_object, colors):
        # result
        res = class_object(CTS1([255, 255, 255], 0), CTS1([0, 0, 0], 0))
        for c in colors:
            if c.r > res.c2.r:
                res.c2.r = c.r
            if c.r < res.c1.r:
                res.c1.r = c.r
            if c.g > res.c2.g:
                res.c2.g = c.g
            if c.g < res.c1.g:
                res.c1.g = c.g
            if c.b > res.c2.b:
                res.c2.b = c.b
            if c.b < res.c1.b:
                res.c1.b = c.b
        return res


class CTS:
    pass


# accepts [r,g,b] array and tolerance
# alternate constructor sigs: r, g, b, tol OR color-number, tol
class CTS1(CTS):
    def __init__(self, color, tol):
        """Initialize a color with a color tolerance speed of 1.

        Keyword arguments:
        color -- the base RGB color in list form [r,g,b]
        tol   -- the tolerance for all the color channels
        """
        for i in range(len(color)):
            v = color[i]  # value
            if v > 255:
                color[i] = 255
            if v < 0:
                color[i] = 0
        self.color = np.array(color, "uint8")
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.tol = tol
        m = []  # min
        M = []  # max
        # handle overflow/underflow
        for i in range(len(self.color)):  # there has to be a more elegant way to do this
            v = self.color[i]
            if v+tol > 255:
                M.append(255)
            else:
                M.append(v + tol)
            if v-tol < 0:
                m.append(0)
            else:
                m.append(v - tol)
        self.min = np.array(m, "uint8")
        self.max = np.array(M, "uint8")

    @classmethod  # accepts an array of CTS1 colors & calcs best color -- equiv to BestColor_CTS1
    def from_colors(class_object, colors):
        """Initialize a CTS1 color that contains the colors provided

        Keyword arguments:
        colors -- the colors used generate the color
        """
        cube = RGBCube.from_colors(colors)
        r = (cube.c1.r + cube.c2.r) // 2
        g = (cube.c1.g + cube.c2.g) // 2
        b = (cube.c1.b + cube.c2.b) // 2
        tol = math.ceil(math.sqrt((r-cube.c1.r)**2 + (g-cube.c1.g)**2 + (b-cube.c1.b)**2))
        return class_object([r, g, b], tol)


# CTS2 but with a tolerance for each color channel instead of just one
# could use HSL instead of rgb here, but IMO not worth the effort
# color space is color space, doesn't matter if it's HSL or RGB
class CTS2(CTS):
    def __init__(self, color, rtol, gtol, btol):
        """Initialize a color with a color tolerance speed of 2.

        Keyword arguments:
        color -- the base RGB color in list form [r,g,b]
        rtol -- the tolerance for the red channel
        gtol -- the tolerance for the green channel
        btol -- the tolerance for the blue channel
        """

        for i in range(len(color)):
            v = color[i]  # value
            if v > 255:
                color[i] = 255
            if v < 0:
                color[i] = 0
        self.color = np.array(color, "uint8")
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]
        self.rtol = rtol
        self.gtol = gtol
        self.btol = btol

        m = []  # min color
        M = []  # max color
        # handle over and underflow
        if self.r+self.rtol > 255:  # calc red range
            M.append(255)
        else:
            M.append(self.r+self.rtol)
        if self.r-self.rtol < 0:
            m.append(0)
        else:
            m.append(self.r-self.rtol)

        if self.g+self.gtol > 255:  # calc green range
            M.append(255)
        else:
            M.append(self.g+self.gtol)
        if self.g-self.gtol < 0:
            m.append(0)
        else:
            m.append(self.g-self.gtol)

        if self.b+self.btol > 255:  # calc blue range
            M.append(255)
        else:
            M.append(self.b+self.btol)
        if self.b-self.btol < 0:
            m.append(0)
        else:
            m.append(self.b-self.btol)

        self.min = np.array(m, "uint8")  # the min color according to tolerance
        self.max = np.array(M, "uint8")  # the max color according to tolerance

    def asarray(self) -> List:
        return [self.r, self.g, self.b, self.rtol, self.gtol, self.btol]

    def __str__(self) -> str:
        return str(self.asarray())

    @classmethod  # accepts an array of CTS2 colors & calcs best color -- equiv to BestColor_CTS2
    def from_colors(class_object, colors):
        """Initialize a CTS2 color that contains the colors provided

        Keyword arguments:
        colors -- the colors used generate the color
        """
        cube = RGBCube.from_colors(colors)
        r = np.uint8((int(cube.c1.r) + int(cube.c2.r)) // 2)
        g = np.uint8((int(cube.c1.g) + int(cube.c2.g)) // 2)
        b = np.uint8((int(cube.c1.b) + int(cube.c2.b)) // 2)
        rtol = None
        if r - cube.c1.r < 0:
            rtol = 0
        else:
            rtol = r - cube.c1.r
        gtol = None
        if g - cube.c1.g < 0:
            gtol = 0
        else:
            gtol = g - cube.c1.g
        btol = None
        if b - cube.c1.b < 0:
            btol = 0
        else:
            btol = b - cube.c1.b
        return class_object([r, g, b], rtol, gtol, btol)
