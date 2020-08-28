import PIL
import numpy as np
import numpy.ma as ma
# import png


class ShapeError(Exception):
    def __init__(self, size: tuple):
        super().__init__('''Expected RGB Bitmap with shape (row, col, 3),
                         got {} instead.'''.format(size))


# basically a numpy array with some PIL.PIL.Image functions added
# NOTE: MaskedArray is a subclass of ndarray
class Image(ma.MaskedArray):
    """
    Represents an RGB image/bitmap.

    ...

    Note
    ----
        construct with Image(array) or array.view(Image)


    Attributes
    ----------
        open(fname)
            create a Image from a disk file
        frombytes(bytes)
            create a Image from a bytes object
    """
    def __new__(class_object, data: np.ndarray):
        obj = super().__new__(class_object, data, dtype='uint8')
        # obj.attr = None
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        # Note that it is here, rather than in the __new__ method,
        # that we set the default value for 'attr', because this
        # method sees all creation of default objects - with the
        # MaskedArray.__new__ constructor, but also with
        # arr.view(InfoArray).
        # self.attr = getattr(obj, 'attr', None)
        # We do not need to return anything
        super().__array_finalize__(obj)

    @classmethod
    def open(class_object, fname: str):
        img = PIL.Image.open(fname).convert('RGB')
        img = ma.array(img, dtype='uint8')
        return class_object(img)

    @classmethod
    def frombytes(class_object, size: tuple, data):
        img = PIL.Image.frombytes('RGB', size, data, 'raw', 'BGRX')
        img = img.convert('RGB')
        img = ma.array(img, dtype='uint8')
        return class_object(img)

    def save(self, fname='untitled'):
        if '.' in fname:
            fname = fname.split()[0]
        PIL.Image.fromarray(self).save(fname)
        # png.from_array(self, mode='RGB').save(fname + '.png')

    def show(self, title=None):
        # NOTE: image.show window titles dont work on my machine
        PIL.Image.fromarray(self).show(title)
