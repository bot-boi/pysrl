# color finders and color tolerance speed definitions
import numpy as np
# from core.types.point_array import PointArray
from core.types.box import Box


# returns points of a PIL Image that're within color +/- tolerance & bounds
def find_colors(arr: np.ndarray, color, bounds=None):
    """Find locations of pixels in an image within a color range.

    Keyword arguments:
    img    -- The PIL image to be searched.
    color  -- The color range to be looked for.
    bounds -- The area in img that will be searched for color, default area is entire image.
    """
    (h, w, _) = np.shape(arr)
    if bounds is None:
        bounds = Box.from_array([0, 0, w, h])
    b = bounds
    arr = arr[b.y1:b.y2, b.x1:b.x2]  # apply bounds
    x, y = np.where(np.all(np.logical_and(np.less_equal(arr, color.max), np.greater_equal(arr, color.min)), 2))
    points = np.column_stack((x, y))
    return points
    # return PointArray.from_array(points)
