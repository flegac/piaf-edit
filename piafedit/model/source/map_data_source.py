from piafedit.model.libs.operator import Operator, Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.source_infos import SourceInfos
from piafedit.model.source.window import Window


class MapDataSource(DataSource):

    def __init__(self, source: DataSource, operator: Operator):
        super().__init__()
        self.source = source
        self.operator = operator

    def infos(self) -> SourceInfos:
        return self.source.infos()

    def read_at(self, window: Window = None) -> Buffer:
        buffer = self.source.read_at(window)
        buffer = self.operator(buffer)
        return buffer

    def write_at(self, buffer: Buffer, window: Window = None):
        buffer = self.operator(buffer)
        return self.source.write_at(buffer, window)
