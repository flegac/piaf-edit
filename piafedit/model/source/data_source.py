from abc import ABC, abstractmethod
from typing import Union, Tuple

from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator, Buffer


class DataSource(ABC):
    def map(self, operator: Operator) -> 'DataSource':
        from piafedit.model.source.map_data_source import MapDataSource
        return MapDataSource(self, operator)

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def bands(self) -> int:
        ...

    @abstractmethod
    def dtype(self):
        ...

    @abstractmethod
    def shape(self) -> Tuple[int, int, int]:
        ...

    @abstractmethod
    def size(self) -> SizeAbs:
        ...

    @abstractmethod
    def read(self, window: Union[Rect, RectAbs] = None, output_size: SizeAbs = None) -> Buffer:
        ...

    @abstractmethod
    def write(self, buffer: Buffer, window: Union[Rect, RectAbs] = None):
        ...

    def overview_size(self, size: int) -> SizeAbs:
        aspect = self.size().aspect_ratio
        if aspect > 1:
            w, h = size, size / aspect
        else:
            w, h = size * aspect, size
        return SizeAbs(w, h)

    def overview(self, size: int):
        overview_size = self.overview_size(size)
        overview = self.read(output_size=overview_size)
        return overview
