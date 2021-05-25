import logging
import uuid

from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.source_infos import SourceInfos
from piafedit.model.source.window import Window

log = logging.getLogger()


class RawDataSource(DataSource):

    def __init__(self, data: Buffer):
        super().__init__()
        self.data = data
        self._infos = SourceInfos(
            name=str(uuid.uuid4()),
            dtype=str(data.dtype),
            shape=data.shape
        )

    def infos(self) -> SourceInfos:
        return self._infos

    def write_at(self, buffer: Buffer, window: Window = None):
        data = self.update_window(window).crop(self.data)
        data[...] = buffer

    def read_at(self, window: Window = None) -> Buffer:
        import cv2
        data = self.update_window(window).window.crop(self.data)
        if window.size:
            data = cv2.resize(data, dsize=window.size.raw(), interpolation=cv2.INTER_CUBIC)
        return data
