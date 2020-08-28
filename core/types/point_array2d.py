# array of point arrays -- equivalent to SRL's T2DPointArray
import numpy as np
import numpy.ma as ma
from .error import NumpyShapeError
from .image import Image


class PointArray2D(ma.MaskedArray):
    def __new__(class_object, data):
        print(ma.shape(data))
        if data.shape[2] != 2:
            raise NumpyShapeError('(parray, point, x/y)', data.shape)
        obj = super(PointArray2D, class_object) \
            .__new__(class_object, data, dtype='uint8')
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        super().__array_finalize__(obj)

    # TODO: make this return a PointArray2D
    def filtersize(self, m, M):  # removes clusters outside range m/M
        sizes = np.array([len(pa) for pa in self])  # cluster sizes
        m1 = sizes < m
        m2 = sizes > M
        mask = ~(m1 | m2)
        return self[mask]

    def draw(self, img: Image) -> Image:
        img = img.copy()
        for c in self:
            color = np.random.randint(0, 255, 3, dtype="uint8")
            for p in c:
                img[p[1], p[0]] = color
        return img
