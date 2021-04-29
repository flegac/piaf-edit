from copy import deepcopy
from typing import Union, Tuple

import cv2

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs, Rect
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.raw_data_source import RawDataSource


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
        source_size = self.source.size()
        roi = deepcopy(self.roi).limit(source_size)

        if window:
            if isinstance(window, Rect):
                window = window.abs(roi.size)
            window.pos.x += roi.pos.x
            window.pos.y += roi.pos.y
        else:
            window = roi
        return self.source.read(window, output_size)

    def write(self, buffer: Buffer, window: Union[Rect, RectAbs] = None):
        source_size = self.source.size()
        roi = deepcopy(self.roi).limit(source_size)

        if window:
            if isinstance(window, Rect):
                window = window.abs(roi.size)
            window.pos.x += roi.pos.x
            window.pos.y += roi.pos.y
        else:
            window = roi
        return self.source.write(buffer, window)


import numpy as np

if __name__ == '__main__':
    buffer = np.random.random((6, 6, 3)) * 255
    cv2.imwrite('test.png', buffer)

    source = RawDataSource(buffer)
    source2 = RoiDataSource(source)
    source2.roi = RectAbs.from_raw(((1, 1), (4, 4)))
    buff = source2.read(RectAbs.from_raw(((1, 1), (2, 2))))
    cv2.imwrite('out.png', buff)
