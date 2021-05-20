from copy import deepcopy

import cv2

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs, Rect
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.raw_data_source import RawDataSource
from piafedit.model.source.source_infos import SourceInfos


class RoiDataSource(DataSource):
    def __init__(self, source: DataSource):
        self.source = source
        self.roi = RectAbs(PointAbs(0, 0), source.infos().size)

    def infos(self) -> SourceInfos:
        b = self.source.infos().bands
        w, h = self.roi.size.raw()
        return SourceInfos(
            name=self.source.infos().name,
            dtype=self.source.infos().dtype,
            shape=(b, h, w),
        )

    def read(self, window: RectAbs = None, output_size: SizeAbs = None) -> Buffer:
        source_size = self.source.infos().size
        roi = deepcopy(self.roi).limit(source_size)

        if window:
            if isinstance(window, Rect):
                window = window.abs(roi.size)
            window.pos.x += roi.pos.x
            window.pos.y += roi.pos.y
        else:
            window = roi
        return self.source.read(window, output_size)

    def write(self, buffer: Buffer, window: RectAbs = None):
        source_size = self.source.infos().size
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
