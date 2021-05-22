from dataclasses import dataclass

from piafedit.model.geometry.rect import RectAbs
from piafedit.model.geometry.size import SizeAbs, Size


@dataclass
class Window:
    window: RectAbs = None
    size: SizeAbs = None

    def set_max_size(self, max_size: int):
        aspect = Size.from_aspect(self.aspect_ratio)
        self.size = aspect.abs(SizeAbs(max_size, max_size))

    @property
    def aspect_ratio(self):
        return self.window.aspect_ratio

    @staticmethod
    def from_window(window: RectAbs):
        return Window(window=window)

    @staticmethod
    def from_size(size: SizeAbs):
        return Window(size=size)
