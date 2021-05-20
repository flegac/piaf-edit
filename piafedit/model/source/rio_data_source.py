import logging
import warnings
from pathlib import Path

import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.profiles import DefaultGTiffProfile
from rasterio.windows import Window

from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.source_infos import SourceInfos

warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)

log = logging.getLogger()
logging.getLogger('rasterio').setLevel(logging.WARNING)


class RIODataSource(DataSource):
    def __init__(self, path: Path):
        self.path = path
        self.resampling: Resampling = Resampling.cubic

        self._infos = None
        if path.exists():
            with rasterio.open(self.path) as src:
                w = src.width
                h = src.height
                b = src.count
                self._infos = SourceInfos(
                    name=self.path.stem,
                    shape=(h, w, b),
                    dtype=src.dtypes[0]
                )

    def create(self, buffer: Buffer):
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
                    factors = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
                    dst.build_overviews(factors, Resampling.average)
                    dst.update_tags(ns='rio_overview', resampling='average')
                    break

    def infos(self) -> SourceInfos:
        if not self._infos:
            with rasterio.open(self.path) as src:
                w = src.width
                h = src.height
                b = src.count
                self._infos = SourceInfos(
                    name=self.path.stem,
                    shape=(h, w, b),
                    dtype=src.dtypes[0]
                )
        return self._infos

    def write(self, buffer: Buffer, window: RectAbs = None):
        window = None
        infos = self.infos()
        if window:
            if isinstance(window, Rect):
                window = window.abs(infos.size)
            window = window_from_rect(window)

        width, height = infos.size.raw()
        shape = buffer.shape
        bands = 1 if len(shape) <= 2 else shape[2]
        with rasterio.open(self.path, 'w', driver='GTiff',
                           width=width, height=height, count=bands,
                           dtype=buffer.dtype) as dst:
            dst.write(buffer, window=window, indexes=1)

    def read(self, window: RectAbs = None, output_size: SizeAbs = None) -> Buffer:
        # log.debug(f'reading: {window} -> {output_size}')
        if window:
            if isinstance(window, Rect):
                window = window.abs(self.infos().size)
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
