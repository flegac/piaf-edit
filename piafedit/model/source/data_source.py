from abc import ABC, abstractmethod

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator, Buffer
from piafedit.model.source.source_infos import SourceInfos


class DataSource(ABC):
    def map(self, operator: Operator) -> 'DataSource':
        from piafedit.model.source.map_data_source import MapDataSource
        return MapDataSource(self, operator)

    @abstractmethod
    def infos(self) -> SourceInfos:
        ...

    @abstractmethod
    def read(self, window: RectAbs = None, output_size: SizeAbs = None) -> Buffer:
        ...

    @abstractmethod
    def write(self, buffer: Buffer, window: RectAbs = None):
        ...

    def update_window(self, window: RectAbs = None):
        if window is None:
            window = RectAbs(pos=PointAbs(0, 0), size=self.infos().size)
        return window

    def overview_size(self, size: int) -> SizeAbs:
        aspect = self.infos().aspect
        if aspect > 1:
            w, h = size, size / aspect
        else:
            w, h = size * aspect, size
        return SizeAbs(w, h)

    def overview(self, size: int):
        overview_size = self.overview_size(size)
        overview = self.read(output_size=overview_size)
        return overview
