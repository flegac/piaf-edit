from abc import ABC, abstractmethod

from piafedit.model.geometry.point import PointAbs
from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs
from piafedit.model.libs.operator import Buffer
from piafedit.model.source.source_infos import SourceInfos
from piafedit.model.source.window import Window


class DataSource(ABC):
    @abstractmethod
    def infos(self) -> SourceInfos:
        ...

    @abstractmethod
    def read_at(self, window: Window = None) -> Buffer:
        ...

    @abstractmethod
    def write_at(self, buffer: Buffer, window: Window = None):
        ...

    def update_window(self, window: Window):
        if window.window is None:
            window.window = RectAbs(pos=PointAbs(0, 0), size=self.infos().size)
        return window

    def overview_size(self, max_size: int) -> SizeAbs:
        aspect = self.infos().aspect
        if aspect > 1:
            w, h = max_size, max_size / aspect
        else:
            w, h = max_size * aspect, max_size
        return SizeAbs(w, h)

    def overview(self, max_size: int):
        window = Window.from_size(self.overview_size(max_size))
        return self.read_at(window)


class WindowSource(DataSource):
    def __init__(self, source: DataSource):
        self.source = source
        self.window: Window = Window()
