import numpy as np

from pysrl.core.font import FONTS
from pysrl.core.types.image import Image
from pysrl.core.types.point import Point


def draw_image(src: Image, insert: Image, pos: Point) -> Image:
    src = src.copy()
    My, Mx, _ = src.shape  # max y, x
    i_h, i_w, _ = insert.shape  # insert height, width
    if pos.x + i_w > Mx or pos.y + i_h > My:
        raise Exception('Can\'t insert image {} into image {} at {},{}') \
            .format(insert.shape, src.shape, pos.x, pos.y)
    else:
        ys = range(0, i_h)
        xs = range(0, i_w)
        for y in ys:
            for x in xs:
                if not np.all(insert.mask[y, x]):
                    src[pos.y + y, pos.x + x] = insert[y, x]
    return src


# convert text to osrs font image
def text_to_img(text: str, fontname='UpChars07') -> Image:
    font = FONTS[fontname]
    height = font['a'].shape[0]
    textimg = np.zeros((height, 0, 3), dtype='uint8')
    for c in text:
        textimg = np.concatenate((textimg, font[c]), axis=1)
    return textimg.view(Image)


def draw_text(img: Image, text: str, pos: Point,
              fontname='UpChars07', color=[255, 0, 0]):
    if type(pos) is tuple:
        pos = Point(pos[0], pos[1])
    img = img.copy()
    textimg = text_to_img(text)
    y, x, _ = np.nonzero(textimg)  # indices of nonblack values
    points = zip(y, x)
    for p in points:
        img[p[0] + pos.y, p[1] + pos.x] = color
    return img
