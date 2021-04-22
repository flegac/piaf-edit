from typing import Union, Tuple

import cv2
import numpy as np

from piafedit.data_source.data_source import DataSource
from piafedit.geometry.point import PointAbs
from piafedit.geometry.rect import RectAbs, Rect
from piafedit.geometry.size import SizeAbs, Size


class SimpleDataSource(DataSource):

    def __init__(self, data: np.ndarray):
        super().__init__()
        self.data = data

    def dtype(self):
        return self.data.dtype

    def shape(self) -> Tuple[int, int, int]:
        return self.data.shape

    def size(self):
        return SizeAbs.from_buffer(self.data)

    def write(self, buffer: np.ndarray, area: Union[Rect, RectAbs] = None):
        if area is None:
            area = RectAbs(pos=PointAbs(0, 0), size=self.size())
        if isinstance(area, Rect):
            area = area.abs(self.size())
        area.crop(self.data)[...] = buffer

    def read(self, area: Union[Rect, RectAbs] = None, out_shape: Union[Size, SizeAbs] = None) -> np.ndarray:
        if area is None:
            area = RectAbs(pos=PointAbs(0, 0), size=self.size())
        if isinstance(area, Rect):
            area = area.abs(self.size())
        buffer = area.crop(self.data)
        if out_shape:
            if isinstance(out_shape, Size):
                out_shape = out_shape.abs(self.size())
            buffer = buffer.astype('uint16')  # TODO: remove this when all is fine
            buffer = cv2.resize(buffer, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)

        return buffer


if __name__ == '__main__':
    area = RectAbs(
        pos=PointAbs(1, 1),
        size=SizeAbs(2, 2)
    )
    data = np.zeros((5, 5))
    source = SimpleDataSource(data)

    out = source.read()
    print(out)

    source.write(np.ones((1, 1)), area)

    out = source.read()
    print(out)
