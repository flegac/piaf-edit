from typing import Union, Tuple

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs, Rect
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource


class RoiDataSource(DataSource):
    def __init__(self, source: DataSource):
        self.source = source
        self.roi = RectAbs(PointAbs(0, 0), source.size())

    def name(self) -> str:
        return f'{self.source.name()}@{self.roi}'

    def bands(self) -> int:
        return self.source.bands()

    def dtype(self):
        return self.source.dtype()

    def shape(self) -> Tuple[int, int, int]:
        w, h = self.roi.size.raw()
        return self.bands(), h, w

    def size(self) -> SizeAbs:
        return self.roi.size

    def read(self, window: Union[Rect, RectAbs] = None, output_size: SizeAbs = None) -> Buffer:
        if window:
            if isinstance(window, RectAbs):
                window = window.rel(self.roi.size)
            window = window.abs(self.roi.size)
        return self.source.read(window, output_size)

    def write(self, buffer: Buffer, window: Union[Rect, RectAbs] = None):
        if window:
            if isinstance(window, RectAbs):
                window = window.rel(self.roi.size)
            window = window.abs(self.roi.size)
        return self.source.write(buffer, window)
