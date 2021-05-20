from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Operator, Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.source_infos import SourceInfos


class MapDataSource(DataSource):

    def __init__(self, source: DataSource, operator: Operator):
        super().__init__()
        self.source = source
        self.operator = operator

    def infos(self) -> SourceInfos:
        return self.source.infos()

    def read(self, window: RectAbs = None, output_size: SizeAbs = None) -> Buffer:
        buffer = self.source.read(window, output_size)
        buffer = self.operator(buffer)
        return buffer

    def write(self, buffer: Buffer, window: RectAbs = None):
        return self.source.write(buffer, window)
