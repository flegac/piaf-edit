from typing import Union, Tuple

import cv2
import numpy as np

from piafedit.model.source.data_source import DataSource
from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs, Rect
from piafedit.model.geometry.size import SizeAbs, Size


class RawDataSource(DataSource):

    def __init__(self, data: np.ndarray):
        super().__init__()
        self.data = data

    def bands(self):
        return self.data.shape[2]

    def dtype(self):
        return self.data.dtype

    def shape(self) -> Tuple[int, int, int]:
        return self.data.shape

    def size(self):
        return SizeAbs.from_buffer(self.data)

    def write(self, buffer: np.ndarray, window: Union[Rect, RectAbs] = None):
        if window is None:
            window = RectAbs(pos=PointAbs(0, 0), size=self.size())
        if isinstance(window, Rect):
            window = window.abs(self.size())
        window.crop(self.data)[...] = buffer

    def read(self, window: Union[Rect, RectAbs] = None, output_size: Union[Size, SizeAbs] = None) -> np.ndarray:
        if window is None:
            window = RectAbs(pos=PointAbs(0, 0), size=self.size())
        if isinstance(window, Rect):
            window = window.abs(self.size())
        buffer = window.crop(self.data)
        if output_size:
            if isinstance(output_size, Size):
                output_size = output_size.abs(self.size())
            buffer = buffer.astype('uint16')  # TODO: remove this when all is fine
            buffer = cv2.resize(buffer, dsize=output_size.raw(), interpolation=cv2.INTER_CUBIC)

        return buffer


if __name__ == '__main__':
    area = RectAbs(
        pos=PointAbs(1, 1),
        size=SizeAbs(2, 2)
    )
    data = np.zeros((5, 5))
    source = RawDataSource(data)

    out = source.read()
    print(out)

    source.write(np.ones((1, 1)), area)

    out = source.read()
    print(out)
