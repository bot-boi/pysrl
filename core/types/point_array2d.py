# array of point arrays -- equivalent to SRL's T2DPointArray
import numpy as np
import numpy.ma as ma
from .error import NumpyShapeError
from .image import Image


class PointArray2D(ma.MaskedArray):
    def __new__(class_object, data: np.ndarray):
        if data.shape[2] != 2:
            raise NumpyShapeError('(parray, point, x/y)', data.shape)
        obj = super().__new__(class_object, data, dtype='uint8') \
            .view(class_object)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        super().__array_finalize__(obj)

    # TODO: make this return a PointArray2D
    def filtersize(self, m, M):  # removes clusters outside range m/M
        for i, pa in enumerate(self):
            length = len(pa)
            if length < m and length > M:
                self.mask[i] = True
        return self

    def draw(self, img: Image) -> Image:
        img = img.copy()
        for c in self:
            color = np.random.randint(0, 255, 3, dtype="uint8")
            for p in c:
                img[p[0], p[1]] = color
        return img
