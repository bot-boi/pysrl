# array of points -- equivalent to SRL's TPointArray
import numpy as np
import numpy.ma as ma
from .point import Point
from .error import NumpyShapeError
from .image import Image
from .box import Box
from .point_array2d import PointArray2D


class PointArray(ma.MaskedArray):
    def __new__(class_object, data: np.ndarray):
        if data.shape[1] != 2:
            raise NumpyShapeError('(rows, 2)', data.shape)
        obj = super().__new__(class_object, data, dtype='uint8') \
            .view(class_object)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        super().__array_finalize__(obj)

    def bounds(self) -> Box:
        mx = self[0][0]  # m/M starting values
        Mx = self[0][0]
        my = self[0][1]
        My = self[0][1]
        for p in self:
            x = p[0]
            y = p[1]
            if x < mx:
                mx = x
            elif x > Mx:
                Mx = x
            if y < my:
                my = y
            elif y > My:
                My = y
        return Box(Point(mx, my), Point(Mx, My))

    # clustering algorithm by benland100
    def cluster(self: np.ndarray, radius=5,
                bnds: Box = None) -> PointArray2D:

        if bnds is not None:
            self = bnds.contains(self)
        clusters = np.zeros(len(self), dtype='uint32')
        while True:  # loop until all self are clustered
            unclustered = clusters == 0
            remaining = np.count_nonzero(unclustered)
            if remaining == 0:
                break
            # any self near this group (and their self) become a new group
            # do this randomly to save time
            candidate = self[unclustered][np.random.randint(remaining)]
            dist = np.sum(np.square(self-candidate), axis=1)
            # importantly includes candidate point
            nearby_mask = dist <= radius*radius
            # groups that were close
            overlaps = set(list(clusters[nearby_mask]))
            overlaps.remove(0)
            if len(overlaps) == 0:
                G = np.max(clusters)+1  # new cluster
            else:
                G = np.min(list(overlaps))  # prefer smaller numbers
            # set all nearby clusters to index G
            clusters[nearby_mask] = G
            for g in overlaps:
                if g == G or g == 0:
                    continue
                clusters[clusters == g] = G
        unique, counts = np.unique(clusters, return_counts=True)
        cluster_points = np.array([self[clusters == c] for c in unique])
        return PointArray2D(cluster_points)  # , counts

    def draw(self, img: Image, color=[255, 0, 0]) -> Image:
        img = img.copy()
        for p in self:
            img[p[0], p[1]] = color
        return img
