import logging
import warnings
from pathlib import Path
from typing import Union, Tuple

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.profiles import DefaultGTiffProfile
from rasterio.windows import Window

from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.source.data_source import DataSource

warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)

log = logging.getLogger()


class RIODataSource(DataSource):
    def __init__(self, path: Path):
        super().__init__(path.stem)
        self.path = path
        self.resampling: Resampling = Resampling.cubic

    def create(self, buffer: np.ndarray):
        h, w = buffer.shape[:2]
        count = 1
        if len(buffer.shape) >= 2:
            count = buffer.shape[2]
        size = SizeAbs(w, h)
        with rasterio.open(self.path, 'w',
                           **DefaultGTiffProfile(
                               tiled=True,
                               width=size.width,
                               height=size.height,
                               count=count,
                               dtype=buffer.dtype,
                               driver='GTiff'
                           )) as dst:
            for i in range(count):
                data = buffer[..., i]
                dst.write(data, i + 1)

        self.create_overview()

    def create_overview(self):
        with rasterio.open(self.path, 'r+') as dst:
            for i in dst.indexes:
                over = dst.overviews(i)
                if over == []:
                    log.debug(f'overview created for {self.path}')
                    factors = [2, 4, 8, 16, 32, 64]
                    dst.build_overviews(factors, Resampling.average)
                    dst.update_tags(ns='rio_overview', resampling='average')
                    break

    def bands(self):
        with rasterio.open(self.path) as src:
            return src.count

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

    def write(self, buffer: np.ndarray, window: Union[Rect, RectAbs] = None):
        window = None
        if window:
            if isinstance(window, Rect):
                window = window.abs(self.size())
            window = window_from_rect(window)

        width, height = self.size().raw()
        shape = buffer.shape
        bands = 1 if len(shape) <= 2 else shape[2]
        with rasterio.open(self.path, 'w', driver='GTiff',
                           width=width, height=height, count=bands,
                           dtype=buffer.dtype) as dst:
            dst.write(buffer, window=window, indexes=1)

    def read(self, window: Union[Rect, RectAbs] = None, output_size: SizeAbs = None) -> np.ndarray:
        if window:
            if isinstance(window, Rect):
                window = window.abs(self.size())
            window = window_from_rect(window)

        with rasterio.open(self.path) as src:
            target = None
            # resampling https://rasterio.readthedocs.io/en/latest/topics/resampling.html
            if output_size:
                target = (src.count, output_size.height, output_size.width)
            data = src.read(
                window=window,
                out_shape=target,
                resampling=self.resampling
            )
            data = np.moveaxis(data, 0, 2)
            return data


def window_from_rect(area: RectAbs = None):
    if not area:
        return None
    return Window(*area.pos.raw(), *area.size.raw())
