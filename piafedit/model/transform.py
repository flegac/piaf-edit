from rasterio.enums import Resampling

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.size import Size


class Transform:
    def __init__(self):
        self.offset = PointAbs(0, 0)
        self.zoom = Size()
        self.resampling: Resampling = Resampling.cubic
