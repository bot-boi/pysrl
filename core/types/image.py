import PIL.Image
import numpy as np
import numpy.ma as ma


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
    def __new__(cls, data: np.ndarray, alpha_mask=False):
        obj = super(Image, cls).__new__(cls, data, dtype='uint8')
        obj.alpha_mask = alpha_mask
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.alpha_mask = getattr(obj, 'alpha_mask', False)
        super().__array_finalize__(obj)

    @classmethod
    def open(class_object, fname: str, alpha_mask=False):
        img = PIL.Image.open(fname)
        mask = None
        if alpha_mask:
            npimg = np.array(img)
            alpha_channel = npimg[..., 3]  # we only care about alpha values
            mask = np.zeros(npimg.shape).astype(bool)  # empty mask
            mask = mask[..., :3]
            mask[np.nonzero(alpha_channel)] = True  # mask all opaque values
            mask = np.invert(mask)  # invert mask values

        img = img.convert('RGB')
        img = ma.array(img, dtype='uint8')
        cls = class_object(img, alpha_mask=alpha_mask)
        cls.mask = mask
        return cls

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
