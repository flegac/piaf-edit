from dataclasses import dataclass
from functools import lru_cache
from typing import Union

import numpy as np

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import Rect, RectAbs, RawRect
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource


@dataclass(frozen=True)
class TileConfig:
    size: SizeAbs

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height


class TileSource(DataSource):
    def __init__(self, source: DataSource, config: TileConfig):
        self.source = source
        self.config = config
        self.cache = dict()

    def infos(self):
        return self.source.infos()

    def read(self, window: Union[Rect, RectAbs] = None, output_size: SizeAbs = None) -> Buffer:
        window = self.update_window(window)
        tiles = self._tiles(window)
        lines = []

        h = len(tiles) * self.config.width
        w = len(tiles[0]) * self.config.height
        b = self.source.infos().bands
        shape = (h, w, b)
        buffer = np.zeros(shape)

        for line in tiles:
            for row in line:
                tile = RectAbs.from_raw(row)
                tile_buffer = self._read_tile(row)
                b = tile.crop(buffer)
                if b.shape == tile_buffer.shape:
                    b[...] = tile_buffer
        return buffer[:window.size.height,:window.size.width,...]

    def write(self, buffer: Buffer, window: Union[Rect, RectAbs] = None):
        self.source.write(buffer, window)

    def _tiles(self, rect: RectAbs):
        start = self.point_to_tile(rect.pos)
        end = self.point_to_tile(rect.pos.copy().move(*rect.size.raw()))
        lines = [
            [
                RectAbs(PointAbs(x, y), self.config.size).raw()
                for x in range(start.pos.x, end.pos.x, self.config.width)
            ]
            for y in range(start.pos.y, end.pos.y, self.config.height)
        ]
        return lines

    @lru_cache()
    def _read_tile(self, tile: RawRect):
        return self.source.read(RectAbs.from_raw(tile))

    def point_to_tile(self, pos: PointAbs):
        dx = pos.x % self.config.width
        dy = pos.y % self.config.height
        return RectAbs(
            pos=PointAbs(pos.x - dx, pos.y - dy),
            size=self.config.size
        )
