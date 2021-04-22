import warnings
from pathlib import Path
from typing import Union, Tuple

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.windows import Window

from piafedit.data_source.data_source import DataSource
from piafedit.geometry.rect import Rect, RectAbs
from piafedit.geometry.size import SizeAbs, Size

warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)


class FastDataSource(DataSource):
    def __init__(self, path: Path):
        super().__init__(path.stem)
        self.path = path

    def dtype(self):
        with rasterio.open(self.path) as src:
            return src.dtypes[0]

    def shape(self) -> Tuple[int, int, int]:
        with rasterio.open(self.path) as src:
            w = src.width
            h = src.height
            b = src.count
            return h, w, b

    def size(self) -> SizeAbs:
        with rasterio.open(self.path) as src:
            w = src.width
            h = src.height
            return SizeAbs(w, h)

    def write(self, buffer: np.ndarray, area: Union[Rect, RectAbs] = None):
        window = None
        if area:
            if isinstance(area, Rect):
                area = area.abs(self.size())
            window = window_from_rect(area)

        width, height = self.size().raw()
        shape = buffer.shape
        bands = 1 if len(shape) <= 2 else shape[2]
        with rasterio.open(self.path, 'w', driver='GTiff',
                           width=width, height=height, count=bands,
                           dtype=buffer.dtype) as dst:
            dst.write(buffer, window=window, indexes=1)

    def read(self, area: Union[Rect, RectAbs] = None, out_shape: Union[Size, SizeAbs] = None) -> np.ndarray:
        # TODO: resampling https://rasterio.readthedocs.io/en/latest/topics/resampling.html
        window = None
        if area:
            if isinstance(area, Rect):
                area = area.abs(self.size())
            window = window_from_rect(area)

        with rasterio.open(self.path) as src:
            target = None

            if out_shape:
                if isinstance(out_shape, Size):
                    out_shape = out_shape.abs(self.size())
                target = (src.count, out_shape.height, out_shape.width)
            data = src.read(
                window=window,
                out_shape=target,
                resampling=Resampling.bilinear
            )
            data = np.moveaxis(data, 0, 2)
            return data


def window_from_rect(area: RectAbs = None):
    if not area:
        return None
    return Window(*area.pos.raw(), *area.size.raw())
