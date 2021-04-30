import logging
import uuid
from typing import Union

import cv2

from piafedit.model.geometry.rect import RectAbs, Rect
from piafedit.model.geometry.size import SizeAbs, Size
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.data_source import DataSource
from piafedit.model.source.source_infos import SourceInfos

log = logging.getLogger()


class RawDataSource(DataSource):

    def __init__(self, data: Buffer):
        super().__init__()
        self.data = data
        self._infos = SourceInfos(
            name=str(uuid.uuid4()),
            dtype=data.dtype,
            shape=data.shape
        )

    def infos(self) -> SourceInfos:
        return self._infos

    def write(self, buffer: Buffer, window: Union[Rect, RectAbs] = None):
        data = self.update_window(window).crop(self.data)
        data[...] = buffer

    def read(self, window: Union[Rect, RectAbs] = None, output_size: Union[Size, SizeAbs] = None) -> Buffer:
        data = self.update_window(window).crop(self.data)
        if output_size:
            if isinstance(output_size, Size):
                output_size = output_size.abs(self.infos().size)
            data = cv2.resize(data, dsize=output_size.raw(), interpolation=cv2.INTER_CUBIC)
        return data
