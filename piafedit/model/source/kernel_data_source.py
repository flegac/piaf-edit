from typing import Tuple, Union

import numpy as np
from scipy.ndimage import convolve

from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.data_source import DataSource


class KernelDataSource(DataSource):
    def __init__(self, source: DataSource, kernel: np.ndarray):
        super().__init__(source.name)
        self.source = source
        self.kernel = kernel

    def bands(self) -> int:
        return self.source.bands()

    def dtype(self):
        return self.source.dtype()

    def shape(self) -> Tuple[int, int, int]:
        return self.source.shape()

    def size(self) -> SizeAbs:
        return self.source.size()

    def read(self, window: Union[Rect, RectAbs] = None, output_size: SizeAbs = None) -> np.ndarray:
        buffer = self.source.read(window, output_size)
        for i in range(buffer.ndim):
            buffer[...,i] = convolve(buffer[...,i], self.kernel) - sum(sum(self.kernel)) + 1
        return buffer

    def write(self, buffer: np.ndarray, window: Union[Rect, RectAbs] = None):
        return self.source.write(buffer, window)