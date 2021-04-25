from typing import Tuple, Union

from piafedit.model.geometry.rect import Rect, RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator, Buffer
from piafedit.model.source.data_source import DataSource


class MapDataSource(DataSource):
    def __init__(self, source: DataSource, operator: Operator):
        super().__init__()
        self.source = source
        self.operator = operator

    def name(self) -> str:
        return self.source.name()

    def bands(self) -> int:
        return self.source.bands()

    def dtype(self):
        return self.source.dtype()

    def shape(self) -> Tuple[int, int, int]:
        return self.source.shape()

    def size(self) -> SizeAbs:
        return self.source.size()

    def read(self, window: Union[Rect, RectAbs] = None, output_size: SizeAbs = None) -> Buffer:
        buffer = self.source.read(window, output_size)
        buffer = self.operator(buffer)
        return buffer

    def write(self, buffer: Buffer, window: Union[Rect, RectAbs] = None):
        return self.source.write(buffer, window)
